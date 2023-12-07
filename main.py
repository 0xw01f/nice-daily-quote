import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from instabot import Bot
import shutil



def get_random_quote():
    while True:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        quote_id = data['_id']

        # Check if the quote ID is already in the file
        if os.path.exists('quote_ids.txt'):
            with open('quote_ids.txt', 'r') as file:
                existing_ids = file.read().splitlines()
                if quote_id in existing_ids:
                    continue

        # Write the quote ID into the file
        with open('quote_ids.txt', 'a') as file:
            file.write(quote_id + '\n')

        return data['content'], data['author'], quote_id


def generate_images(base_image_path, output_folder, font_path, max_font_size, max_text_width, style_mode):
     # Get a random quote
    quote, author, quote_id = get_random_quote()

    # Open the base image
    base_image = Image.open(base_image_path)
    
    # Create a drawing object
    draw = ImageDraw.Draw(base_image)

    # Calculate maximum possible font size based on the image dimensions
    quote_font_size = min(max_font_size, base_image.width // 20, base_image.height // 20)
    author_font_size = min(max_font_size, base_image.width // 30, base_image.height // 30)



    # Calculate quote and author positions

    # Adjust quote position if the qote is too long

    if len(quote) > 350:
        quote_position = ((base_image.width / 4) // 2, (base_image.height / 5))
    elif len(quote) > 160:
        quote_position = ((base_image.width / 4) // 2, (base_image.height / 3))
    else :
        quote_position = ((base_image.width / 2) // 2, (base_image.height / 3))


    
    # Adjust author position if the quote is too long
    if len(quote) < 60 :
        author_position = ((base_image.width * 2.2 / 4) - 60, (base_image.height / 2))
    elif len(quote) > 60 and len(quote) < 100:
        author_position = ((base_image.width * 2.2 / 4) - 60, (base_image.height / 1.9))
    elif len(quote) > 220:
        author_position = ((base_image.width * 2.2 / 4) - 60, (base_image.height / 1.2))
    else:
        author_position = ((base_image.width * 2.2 / 4) - 30, (base_image.height / 1.6))

    # Draw the wrapped quote on the image
    draw = ImageDraw.Draw(base_image)

    if (len(quote) > 160):
        wrapped_quote = textwrap.fill(quote, width=40)
    else:
        wrapped_quote = textwrap.fill(quote, width=30) 


    if style_mode == "dark":
        # Create a dark background rectangle
        dark_background = Image.new('RGBA', base_image.size, (0, 0, 0, 150))
        base_image.paste(dark_background, (0, 0), dark_background)
        draw.text(quote_position, wrapped_quote, font=ImageFont.truetype(font_path, quote_font_size), fill=(255, 255, 255))
        # Draw the author text on the left side
        draw.text(author_position, author, font=ImageFont.truetype(font_path, author_font_size), fill=(255, 255, 255))
    
    elif style_mode == "light":
        draw.text(quote_position, wrapped_quote, font=ImageFont.truetype(font_path, quote_font_size), fill=(73, 73, 73))
        # Draw the author text on the left side
        draw.text(author_position, author, font=ImageFont.truetype(font_path, author_font_size), fill=(73, 73, 73))
    




    # Save the image with a filename containing the author's name, the quote ID, and today's date
    filename = f"{author}_{quote_id}_{datetime.now().strftime('%Y-%m-%d')}.jpg"
    base_image.save(os.path.join(output_folder, filename))


    print(f"Image generated successfully.")
    publish_images(insta_username, insta_password, author)

def publish_images(insta_username, insta_password, author):
    # Delete config folder
    config_path = "./config"
    shutil.rmtree(config_path)


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
        bot.upload_photo(os.path.join(images_folder_path, filename), caption="✨ Daily Quotes ✨ \n\n📖 \n\n📚 @" + insta_username + "\n\n#quotes #quoteoftheday #quotestoliveby #quotesdaily #quotesaboutlife")


        # Move the image with "REMOVE_ME" to the uploaded folder
        try:
            shutil.move(file_path + ".REMOVE_ME", os.path.join(uploaded_folder_path, filename + ".REMOVE_ME"))
            # Remove the "REMOVE_ME" text in the filename
            os.rename(os.path.join(uploaded_folder_path, filename + ".REMOVE_ME"), os.path.join(uploaded_folder_path, filename))
        except:
            print("File exists or not found")




    bot.logout()

    print(f"Image published successfully.")




# Config
base_image_path = "quote-paper.jpg"
style_mode = "light"
quotes_file_path = "quotes.txt"
output_folder = "output_images"
font_path = "CormorantGaramond-BoldItalic.ttf"
max_font_size = 80
max_text_width = 30

insta_username = "nice_daily_quote"
insta_password = ""

generate_images(base_image_path, output_folder, font_path, max_font_size, max_text_width, style_mode)

