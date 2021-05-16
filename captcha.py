def captchaBuilder(resp):
    import re

    import PySimpleGUI as sg
    from reportlab.graphics import renderPM
    from svglib.svglib import svg2rlg

    with open("captcha.svg", "w") as f:
        f.write(resp["captcha"])

    imgfile = open("captcha.svg", "r+")

    captcha_cleaned = re.sub('(<path d=)(.*?)(fill="none"/>)', "", imgfile.read())

    imgfile.seek(0)

    imgfile.write(captcha_cleaned)

    imgfile.truncate()

    imgfile.close()

    drawing = svg2rlg("captcha.svg")

    renderPM.drawToFile(drawing, "captcha.png", fmt="PNG")

    layout = [
        [sg.Image("captcha.png")],
        [sg.Text("Enter Captcha Below")],
        [sg.Input(key="txtcaptcha")],
        [sg.Button("Submit", bind_return_key=True)],
    ]

    window = sg.Window("Enter Captcha", layout, finalize=True)
    window.TKroot.focus_force()  # focus on window
    window.Element("txtcaptcha").SetFocus()  # focus on field

    event, values = window.read()

    window.close()

    return values["txtcaptcha"]
