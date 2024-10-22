# noqa


import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_gradient_image(width, height, color_dict):
    """Create a gradient image from a color dictionary with float positions and RGB values.

    :param width: Width of the image.
    :param height: Height of the image.
    :param color_dict: A dictionary with float positions as keys (0.0 to 1.0) and RGB tuples as values.
    :return: A Pillow Image object.
    """
    # Create a blank image
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    draw = ImageDraw.Draw(img)

    # Sort color stops by their position
    stops = sorted(color_dict.keys())

    max_value = max(color_dict.keys())

    # Logarithmic scaling factor
    epsilon = 1e-4
    log_base = 10
    log_min = math.log(epsilon, log_base)  # Logarithmic position for start (to avoid log(0))
    log_max = math.log(0.6 + epsilon, log_base)  # Logarithmic position for end (0.6)

    # Iterate over every pixel in the image
    for x in range(width):
        # Determine the position along the gradient (normalized between 0 and 1)
        pos = x / (width - 1) * max_value

        log_pos = log_min + (x / (width - 1)) * (log_max - log_min)
        pos = (log_base**log_pos) - epsilon

        # Find two stops that the current position falls between
        for i in range(len(stops) - 1):
            if stops[i] <= pos <= stops[i + 1]:
                # Normalize the position between these two stops
                start_pos = stops[i]
                end_pos = stops[i + 1]

                # Get the colors for these stops
                start_color = np.array(color_dict[start_pos])
                end_color = np.array(color_dict[end_pos])

                # Interpolate the color based on the position
                ratio = (pos - start_pos) / (end_pos - start_pos)
                interp_color = (start_color + ratio * (end_color - start_color)).astype(int)

                # Fill the column with the interpolated color
                for y in range(height):
                    pixels[x, y] = tuple(interp_color)
                break

    # Add labels for specified positions (e.g., 0.1 to 0.6)
    font = ImageFont.load_default()
    for label in np.arange(0.0, max_value, 0.05):
        label_x = int((label / max_value) * (width - 1))  # Map label position to x coordinate

        log_label_pos = math.log(label + epsilon, log_base)
        label_x = int((log_label_pos - log_min) / (log_max - log_min) * (width - 1))

        draw.text((label_x, height - 30), f"{ int(label * 100):d}", fill="blue", font=font)
        draw.line(((label_x, height), (label_x, height - 10)))

    return img


dta = {
    0.0: "255,255,255",
    0.003814567556847: "255,255,255",
    0.012052403801856: "255,227,227",
    0.029122709238268: "255,198,198",
    0.056400676538509: "255,170,170",
    0.089827122095269: "255,142,142",
    0.148045641643703: "255,113,113",
    0.215713883121917: "255,85,85",
    0.315637932936843: "255,57,57",
    0.379515881573211: "255,0,0",
    0.602678321028618: "255,0,0",
}


# Example usage
color_stops = {
    0.0: (255, 0, 0),  # Red at the start
    0.5: (0, 255, 0),  # Green in the middle
    1.0: (0, 0, 255),  # Blue at the end
}


color_stops = {stop: [int(v) for v in clr.split(",")] for stop, clr in dta.items()}

# Create the image
width, height = 500, 100  # Example dimensions
gradient_image = create_gradient_image(width, height, color_stops)

# Save or show the image
gradient_image.show()  # To display the image
gradient_image.save("gradient.png")  # To save the image

{
    0.0: "255,255,255",
    0.003814567556847: "255,255,255",
    0.012052403801856: "255,227,227",
    0.029122709238268: "255,198,198",
    0.056400676538509: "255,170,170",
    0.089827122095269: "255,142,142",
    0.148045641643703: "255,113,113",
    0.215713883121917: "255,85,85",
    0.315637932936843: "255,57,57",
    0.379515881573211: "255,0,0",
    0.602678321028618: "255,0,0",
}
