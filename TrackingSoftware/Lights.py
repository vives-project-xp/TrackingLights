

class Lights:
  def __init__(self):

    #Define colors
    self.white = [255, 255, 255]
    self.detectedColors = ["FF0000", "F50000", "C00000"]

    self.lightsJson = {}

    return
  
  def groupingPixels(self, pixels):
    
    self.lightsJson = { 
        "on": True,
        "bri": 100,
        "seg":{"i":[0,100, 'FFFFFF']}}

    # put pixels in groups
    pixels_group = [[]]
    group_index = 0
    for i in range(1, len(pixels)-1):
        pixels_distance = pixels[i] - pixels[i-1]
        #print(pixels_distance)

        # if pixels distance is not greater than 20 pixels group them up
        if(pixels_distance < 40):
            pixels_group[group_index].append(pixels[i-1])
            pixels_group[group_index].append(pixels[i])

        else:
            
            group_index += 1
            pixels_group.append([])
    
        for group in pixels_group:

          if(len(group) < 1):
            break
          
          # Initialize values for image processing
          first_pixel = group[0]
          last_pixel = group[len(group)-1]

          # Divide by 6 > each segment of leds = 6leds
          first_pixel = int(group[0]/6)
          last_pixel = int(group[len(group)-1]/6)

          #Adjust pixels color with fade effect
          self.lightsJson["seg"]["i"].append(first_pixel-3)
          self.lightsJson["seg"]["i"].append(last_pixel+3)
          self.lightsJson["seg"]["i"].append("C00000")

          self.lightsJson["seg"]["i"].append(first_pixel-1)
          self.lightsJson["seg"]["i"].append(last_pixel+1)
          self.lightsJson["seg"]["i"].append("F50000")

          self.lightsJson["seg"]["i"].append(first_pixel)
          self.lightsJson["seg"]["i"].append(last_pixel)
          self.lightsJson["seg"]["i"].append("FF0000")

    return pixels_group

  def getJson(self):
    return self.lightsJson