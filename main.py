import cv2
import pygame
from hand_detector import HandDetector
from trex_game import TRexGame  # game logic

# Initialize camera
cap = cv2.VideoCapture(0)
detector = HandDetector()

# Initialize pygame and game
pygame.init()
game = TRexGame()
game.show_start_screen()

game_active = False  # 🔄 Track if the game is active

# Main loop
while True:
    # 1. Read webcam frame
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)

    # 2. Detect hand + check for fist
    frame, results = detector.find_hands(frame)
    fist_detected = detector.is_fist(results)

    # 3. Show webcam feed
    cv2.imshow("PosePlay | Webcam", frame)

    # 4. Game state handling
    if not game_active:
        # Start the game if gesture or key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game = TRexGame()
                game_active = True
        if fist_detected:
            game = TRexGame()
            game_active = True
    else:
        if not game.is_game_over:
            game.update()
            if fist_detected:
                game.jump()
        else:
            game.game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game = TRexGame()
                    game_active = True

    # 5. Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
