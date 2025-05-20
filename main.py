from onvif import ONVIFCamera
import cv2
from zeep.exceptions import Fault

try:
    # Connect to the ONVIF camera
    cam = ONVIFCamera('192.168.100.112', 80, 'admin', 'Password1')

    # Create media service
    media = cam.create_media_service()

    # Get profiles
    profiles = media.GetProfiles()
    if not profiles:
        print("No profiles returned.")
        exit()

    print("Found profiles:", [p.token for p in profiles])
    profile = profiles[0]  # Use the first profile

    # Set up stream parameters
    stream_setup = {
        'Stream': 'RTP-Unicast',
        'Transport': {'Protocol': 'RTSP'}
    }

    # Prepare request to get stream URI
    request = media.create_type('GetStreamUri')
    request.StreamSetup = stream_setup
    request.ProfileToken = profile.token

    # Get the RTSP stream URI
    stream_uri_response = media.GetStreamUri(request)
    uri = stream_uri_response.Uri
    print("Stream URI:", uri)

    # Open the stream with OpenCV
    cap = cv2.VideoCapture(uri)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to get frame")
            break

        cv2.imshow("Camera Live Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Fault as fault:
    print("ONVIF Fault:", fault)
except Exception as e:
    print("Error:", e)
