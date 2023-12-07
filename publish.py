import shutil
import os
from instabot import Bot
from PIL import Image

# Delete config folder
config_path = "./config"
shutil.rmtree(config_path)

insta_username = "nice_daily_quote"
insta_password = ""

bot = Bot()

bot.login(username=insta_username, password=insta_password)

# Define the image path and the uploaded folder path
images_folder_path = "./output_images"
uploaded_folder_path = "./uploaded"



for filename in os.listdir(images_folder_path):
    file_path = os.path.join(images_folder_path, filename)

    if filename.endswith(".png"):
        # Convert PNG to JPG
        img = Image.open(os.path.join(images_folder_path, filename))
        filename = os.path.splitext(filename)[0] + ".jpg"
        img.save(os.path.join(images_folder_path, filename), "JPEG")


    # Upload the image
    bot.upload_photo(os.path.join(images_folder_path, filename), caption="✨ Daily Quotes ✨ \n\n📚 @nice_daily_quote\n\n#quotes #quoteoftheday #quotestoliveby #quotesdaily #quotesaboutlife")


    # Move the image with "REMOVE_ME" to the uploaded folder
    shutil.move(file_path + ".REMOVE_ME", os.path.join(uploaded_folder_path, filename + ".REMOVE_ME"))

    # Remove the "REMOVE_ME" text in the filename
    os.rename(os.path.join(uploaded_folder_path, filename + ".REMOVE_ME"), os.path.join(uploaded_folder_path, filename))

bot.logout()
