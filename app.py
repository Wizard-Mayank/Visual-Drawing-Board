import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import cv2
import numpy as np
import os
import HandTrackingModule as htm

# 1. Page Configuration
st.set_page_config(page_title="Virtual Paint Pro", layout="wide")

# 2. Advanced CSS to fix Stretching and UI Layout
st.markdown(
    """
    <style>
    /* Force main container to use full width */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
    }

    /* Target the specific WebRTC video container */
    div[data-testid="stVerticalBlock"] > div:has(video) {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    /* Force aspect ratio preservation for video */
    video {
        width: 100% !important;
        max-width: 1280px !important; 
        height: auto !important;      
        object-fit: contain !important;
        border-radius: 12px;
        border: 2px solid #4A4A4A;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #111111;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎨 Virtual Paint Pro")
st.sidebar.title("Controls")

# 3. Load Header Images
folderPath = "Bar"
overlayList = []
if os.path.exists(folderPath):
    files = sorted([f for f in os.listdir(folderPath) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    overlayList = [cv2.imread(os.path.join(folderPath, f)) for f in files]

# 4. Canvas Reset Logic (Stored in session_state)
if st.sidebar.button("Reset / Clear Canvas"):
    st.session_state.clear_canvas = True
else:
    if 'clear_canvas' not in st.session_state:
        st.session_state.clear_canvas = False

# 5. Core Video Processing Class
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        # Initialize Hand Detector
        self.detector = htm.handDetector(detectionCon=0.8, maxHands=1)
        
        # Drawing Variables
        self.xp, self.yp = 0, 0
        self.drawColor = (255, 0, 255) # Default Pink
        self.brushThickness = 15
        self.eraserThickness = 100
        
        # Persistent Internal Canvas
        self.imgCanvas = None 

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1) # Mirror view
        h, w, _ = img.shape

        # Initialize or Wipe Canvas based on actual camera dimensions
        if self.imgCanvas is None or self.imgCanvas.shape[:2] != (h, w) or st.session_state.clear_canvas:
            self.imgCanvas = np.zeros((h, w, 3), np.uint8)
            st.session_state.clear_canvas = False # Handled

        # 1. Detect Hand Landmarks
        img = self.detector.findHands(img)
        lmList, _ = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # Tip of Index (8) and Middle (12) fingers
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            
            # Check which fingers are up
            fingers = self.detector.fingersUp()

            # --- SELECTION MODE (Two fingers up) ---
            if fingers[1] and fingers[2]:
                self.xp, self.yp = 0, 0 # Reset path
                if y1 < 125: # Selection header area
                    if (w * 0.2) < x1 < (w * 0.35):
                        self.drawColor = (255, 0, 255)
                    elif (w * 0.43) < x1 < (w * 0.58):
                        self.drawColor = (255, 100, 0)
                    elif (w * 0.62) < x1 < (w * 0.74):
                        self.drawColor = (0, 255, 0)
                    elif (w * 0.82) < x1 < (w * 0.94):
                        self.drawColor = (0, 0, 0) # Eraser selected

            # --- DRAWING MODE (Only Index finger up) ---
            elif fingers[1] and not fingers[2]:
                # Visual Feedback: Light gray circle for eraser, color circle for brush
                if self.drawColor == (0, 0, 0):
                    cv2.circle(img, (x1, y1), self.eraserThickness // 2, (200, 200, 200), 2)
                else:
                    cv2.circle(img, (x1, y1), 15, self.drawColor, cv2.FILLED)

                # First frame of a stroke
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x1, y1
                
                thickness = self.eraserThickness if self.drawColor == (0,0,0) else self.brushThickness
                
                # Draw on the Canvas
                cv2.line(self.imgCanvas, (self.xp, self.yp), (x1, y1), self.drawColor, thickness)
                
                # Update previous position
                self.xp, self.yp = x1, y1
            else:
                # Reset path when hand is closed or not in drawing posture
                self.xp, self.yp = 0, 0

        # --- MERGING CANVAS WITH VIDEO ---
        imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 20, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        
        # Combine using bitwise operations
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, self.imgCanvas)

        # --- OVERLAY HEADER ---
        if overlayList:
            # Determine which header to show based on drawColor
            header = overlayList[0]
            if self.drawColor == (255, 100, 0) and len(overlayList) > 1: header = overlayList[1]
            elif self.drawColor == (0, 255, 0) and len(overlayList) > 2: header = overlayList[2]
            elif self.drawColor == (0, 0, 0) and len(overlayList) > 3: header = overlayList[3]
            
            # Match header width to current camera width
            h_h, _, _ = header.shape
            header_resized = cv2.resize(header, (w, h_h))
            img[0:h_h, 0:w] = header_resized

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# 6. WebRTC Settings (Standard STUN server)
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# 7. Launch Streamer
ctx = webrtc_streamer(
    key="paint-final",
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIG,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

# 8. Sidebar Status
if ctx.state.playing:
    st.sidebar.success("✅ Camera Active")
else:
    st.sidebar.warning("❌ Camera Stopped")

st.sidebar.info("Tip: Use the 'STOP' button under the video to end the session.")