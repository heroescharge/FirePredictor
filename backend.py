from PIL import Image

from numpy import interp

import pandas as pd

from PIL import ImageDraw

import time

# install library "openpyxl" as well

#open files
def simulate(real_years):
    #df = pd.read_excel("uscities.xlsx")

    #Resize image
    temp_img = Image.open("temperature_map.png")
    #temp_img= temp_img.resize((800, 488), Image.ANTIALIAS)
    temp_width, temp_height = temp_img.size
    temp_rgb = temp_img.convert("RGB")

    humidity_img = Image.open("humidities.png")
    #humidity_img = humidity_img.resize((800, 488), Image.ANTIALIAS)
    hum_width, hum_height = humidity_img.size
    hum_rgb = humidity_img.convert("RGB")

    vegetation_img = Image.open("vegetations.png")
    #vegetation_img= vegetation_img.resize((800, 488), Image.ANTIALIAS)
    veg_width, veg_height = vegetation_img.size
    veg_rgb = vegetation_img.convert("RGB")

    def get_temp_pixels(pixel_x, pixel_y, temp_rgb):
        try:
            r, g, b = temp_rgb.getpixel((pixel_x, pixel_y))
        except:
            return "water"
        if ((r >= 90 and r <= 115) and (g >= 20 and g <= 35) and (b >= 20 and b <= 40)):
            return "dark_red"
        elif ((r >= 170 and r <= 220) and (g >= 45 and g <= 100) and (b >= 35 and b <= 95)):
            return "red"
        elif ((r >= 190 and r <= 235) and (g >= 140 and g <= 165) and (b >= 50 and b <= 70)):
            return "orange"
        elif ((r >= 230 and r <= 245) and (g >= 210 and g <= 235) and (b >= 80 and b <= 95)):
            return "yellow"
        elif ((r >= 25 and r <= 45) and (g >= 65 and g <= 85) and (b >= 145 and b <= 165)):
            return "blue"
        elif ((r >= 85 and r <= 105) and (g >= 160 and g <= 180) and (b >= 125 and b <= 145)):
            return "green"
        elif ((r >= 90 and r <= 110) and (g >= 55 and g <= 75) and (b >= 135 and b <= 150)):
            return "purple"
        elif ((r >= 180 and r <= 220) and (g >= 80 and g <= 105) and (b >= 130 and b <= 160)):
            return "pink"
        elif ((r >= 240 and r <= 255) and (g >= 240 and g <= 255) and (b >= 240 and b <= 255)):
            return "water"
        else:
            return "yellow"


    def get_humidity_pixels(pixel_x, pixel_y, pixel_rgb):
        try:
            r, g, b = pixel_rgb.getpixel((pixel_x, pixel_y))
        except:
            return "water"

        if ((r >= 200 and r <= 210) and (g >= 223 and g <= 233) and (b >= 242 and b <= 252)):
            return ("water")
        elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
            return ("water")
        else:

            if ((r >= 190 and r <= 200) and (g >= 65 and g <= 75) and (b >= 46 and b <= 56)):
                return "red"

            elif ((r >= 233 and r <= 243) and (g >= 155 and g <= 165) and (b >= 59 and b <= 69)):
                return "orange"

            elif ((r >= 248 and r <= 258) and (g >= 236 and g <= 246) and (b >= 76 and b <= 86)):
                return "yellow"

            elif ((r >= 169 and r <= 179) and (g >= 200 and g <= 210) and (b >= 113 and b <= 123)):
                return "light_green"

            elif ((r >= 129 and r <= 139) and (g >= 184 and g <= 194) and (b >= 85 and b <= 95)):
                return "yellow_green"

            elif ((r >= 98 and r <= 108) and (g >= 167 and g <= 177) and (b >= 78 and b <= 88)):
                return "green"

            elif ((r >= 56 and r <= 66) and (g >= 132 and g <= 142) and (b >= 71 and b <= 81)):
                return "dark_green"

            elif ((r >= 48 and r <= 58) and (g >= 127 and g <= 137) and (b >= 172 and b <= 182)):
                return "blue"

            else:
                return "water"


    def get_vegetation_pixels(pixel_x, pixel_y, pixel_rgb):
        # Set up images
        try:
            r, g, b = pixel_rgb.getpixel((pixel_x, pixel_y))
        except:
            return "water"
        if ((r >= 250) and (g >= 250) and (b >= 250)):
            return ("water")
        elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
            return ("water")
        else:
            if ((r <= 5) and (g <= 5) and (b <= 5)):
                return "High"
            elif ((r >= 174 and r <= 194) and (g >= 192 and g <= 212) and (b >= 175 and b <= 195)):
                return "None"
            elif ((r >= 241 and r <= 261) and (g >= 219 and g <= 239) and (b >= 188 and b <= 208)):
                return "High"
            elif ((r >= 220 and r <= 240) and (g >= 211 and g <= 231) and (b >= 159 and b <= 179)):
                return "High"
            elif ((r >= 202 and r <= 222) and (g >= 227 and g <= 247) and (b >= 239 and b <= 259)):
                return "None"
            elif ((r >= 118 and r <= 138) and (g >= 149 and g <= 169) and (b >= 84 and b <= 104)):
                return "Medium-High"
            elif ((r >= 171 and r <= 191) and (g >= 195 and g <= 215) and (b >= 167 and b <= 187)):
                return "Medium"
            elif ((r >= 132 and r <= 152) and (g >= 175 and g <= 195) and (b >= 145 and b <= 165)):
                return "Medium"
            else:
                return "High"

    # START OF SIMULATION

    def get_fire_risk_index(temp_risk, humidity_risk, veg, future_years):
        if (temp_risk == 0) or (humidity_risk == 0):
            return (255, 255, 255)
        temp = temp_risk + 0.2*future_years
        hum = humidity_risk - 0.015*future_years
        hum = max((hum) * 90/5.25 + 10, 0.1)
        temp = (temp) * 90/5.25 + 10
        risk = 400/pow(hum, 1.1) + 0.19*temp

        if (veg == "None"):
            risk *= 0.9
        elif (veg == "Medium"):
            risk *= 0.77
        elif (veg == "Medium-High"):
            risk *= 0.82
        elif (veg == "High"):
            risk *= 1.5
                    
        #GYR color interpolation
        rating = 10 * (risk - 20)/(70 - 20) * 1.5 #1.5 color scale factor
        if (rating > 10):
            rating = 10
        elif (rating < 0):
            rating = 0
        rating = 10 - rating
            #rating = interp(risk, [20, 70], [0, 10])
            
        if (rating > 5):
            parts = (1-((rating-5)/5))
        else:
            parts = rating/5
        #parts = (rating > 5) ? (1-((rating-5)/5)) : rating/5
        parts = round(parts * 255)
        if (rating < 5):
            color = (255, parts, 0)
        elif (rating > 5):
            color = (parts, 255, 0)
        else:
            color = (255,255,0)
        return color
        

    def futureSimulation(real_years):
        future_years = real_years
        future_years = max(future_years, 0)
        if future_years < 10:
            future_years = interp(future_years, [0, 10], [6, 10])
        future_years += 10 #shift by few years for scaling
        blankmap = Image.open("static/blankmap.png")
        
        #Reset blankmap
        draw = ImageDraw.Draw(blankmap)
        
        blankmap = blankmap.resize((800, 488), Image.ANTIALIAS)
        draw.rectangle((0, 488, 800, 0), fill=(255, 255, 255))

        blankmappixels = blankmap.load()

        temp_color_to_fire_risk_index = {"dark_red": 6.25, "red": 5.5, "orange": 4.75,
                                        "yellow": 4, "blue": 3.25, "green": 2.5, "purple": 1.75, "pink": 1, "water": 0}
        color_to_temp = {"dark_red": 72.5, "red": 67.5, "orange": 62.5, "yellow": 57.5,
                        "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5, "water": 0}
        humidity_to_fire_risk_index = {"blue": 1, "dark_green": 1.75, "green": 2.5,
                                    "yellow_green": 3.25, "light_green": 4, "yellow": 4.75, "orange": 5.5, "red": 6.25, "water": 0}
        temp_to_color = {value: key for (key, value) in color_to_temp.items()}

        width, height = blankmap.size
        pixel_rgb = blankmap.convert("RGB")

        # increasing temperature as years continue
        for x in range(0, 800):
            for y in range(0, 488):
                pixel_temp_color = get_temp_pixels(x, y, temp_rgb)
                pixel_humidity_color = get_humidity_pixels(x, y, hum_rgb)
                pixel_color = get_fire_risk_index(temp_color_to_fire_risk_index[pixel_temp_color], humidity_to_fire_risk_index[pixel_humidity_color], get_vegetation_pixels(x, y, veg_rgb), future_years)
                
                blankmappixels[x,y] = pixel_color
        blankmap.save("static/blankmap.png")

    futureSimulation(real_years)
