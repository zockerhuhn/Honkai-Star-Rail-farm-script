from PIL import Image

im = Image.open("Example_ChallengeCompleted.png")
im.resize(1920,1080)
im.save("Example_ChallengeCompletedtest.png", Image.ANTIALIAS)
