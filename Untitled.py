# -*- coding: utf-8 -*-

import ui

PLACEHOLDER_TEXT = """First, we create a View. This is the base class for pretty much everything that you can put on the screen. A vanilla View is just a colored rectangle, but it can also serve as a container for other views (in this case, a button).
We set the view’s name to ‘Demo’, this is what will be shown in the title bar, when the view is presented later.
The view’s background color is set to 'white'. You can use strings (color names and hex), tuples (e.g. (1.0, 0.0, 0.0) for red, (0.0, 1.0, 0.0, 0.5) for half-transparent green), or numbers (e.g. 0.5 for 50% gray). Internally, all these color representations are converted to 4-tuples (r, g, b, a), so when you access the view’s background_color attribute later, you’ll get (1.0, 1.0, 1.0, 1.0), no matter if you set it to 'white', '#ffffff', or just 1.0.
We create a new Button, setting its title with a keyword argument. When you set a title during initialization, its size is automatically adjusted to fit.
By setting the View.center attribute, we set the button’s position relative to its parent. In this case, we use half of the parent’s View.width and View.height attributes to center the button.
Because the view may change its size (e.g. when the device is rotated), we set the button’s View.flex attribute that controls its auto-resizing behavior. In this case, we want the left, right, top, and bottom margins to be flexible, so that the button stays centered in its container.
We set the button’s Button.action attribute to the function that is defined at the top of the script. The function must accept a single parameter, which is conventionally named sender. The parameter will be the button that triggered the event, so you can use a single action for multiple buttons, and determine what to do depending on which button caused the event.
We’re done setting up the button, so we add it as a child of the container view, using the View.add_subview() method.
Finally, we call the View.present() method to get the main view on screen. Views can be presented with different styles. On the iPhone, all views are presented in full-screen, but on the iPad, you can choose between 'sheet', 'popover' and 'fullscreen'.
"""

class CustomIO(object):
    root = None
    txts = None
    inp = None
    out = None
    out_str = ""

    def __init__(self):
        # set up root view
        self.root = ui.View(name="CustomIO", flex="WH")

        # set up text area wrapper view
        self.txts = ui.View(flex="WH")
        self.root.add_subview(self.txts)

        # set up input text field
        self.inp = ui.TextField(flex="WT")
        self.txts.add_subview(self.inp)
        self.inp.height = 32
        self.inp.y = self.inp.superview.height - (self.inp.height + 14)
        self.inp.background_color='red'
        self.inp.bordered = False

        # set up output text view
        self.out = ui.TextView()
        self.txts.add_subview(self.out)
        self.out.height = self.out.superview.height - (self.inp.height + 14)
        self.out.flex = "WH"
        self.out.editable = False
        self.out.auto_content_inset=True 


        # set up common text area settings
        self.out.delegate = self.inp.delegate = self

    def run(self):
        self.root.present("panel")
        self.inp.begin_editing()

    # output stream methods
    softspace = 0

    def flush(self):
        co=self.out.content_size[1]
        self.out.text = self.out_str
        @ui.in_background
        def scroll():
            self.out.content_offset = (0, self.out.content_size[1] -self.out.height) # this is the bugged line
        scroll()
    def write(self, data):
        self.out_str += data

    def writelines(self, lines):
        for line in lines:
            self.write(line + "\n")

    # ui.TextField.delegate methods
    def textfield_did_begin_editing(self, textfield):
        if textfield == self.inp:
            # adjust text field not to be covered by onscreen keyboard
            def _set_frame():
                kbf = ui.get_keyboard_frame()
                if kbf[1] > 0:
                    self.txts.height = self.root.height - kbf[3]
            ui.delay(_set_frame, 0.55) # wait for the keyboard to slide up

    def textfield_should_return(self, textfield):
        self.write(PLACEHOLDER_TEXT)
        self.flush()
        #ui.delay(self.flush,0.55)
        return True 

    def scrollview_did_scroll(self,scrollview):
        import console
       # console.hud_alert('{}/{}={}'.format(scrollview.content_offset[1],scrollview.content_size[1],scrollview.content_size[1]-scrollview.content_offset[1]))
if __name__ == "__main__":
    global io

    io = CustomIO()
    io.run()
