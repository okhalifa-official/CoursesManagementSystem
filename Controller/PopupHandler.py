import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from View import PopupView
def confirmation_popup(parent, title="Confirmation", message="Are you sure?", button1_text="No", button2_text="Yes"):
    popup_view = PopupView.PopupView(parent, title=title, message=message, 
                                     button1_text=button1_text, button2_text=button2_text)
    
    # Wait for the popup to be destroyed
    parent.wait_window(popup_view)
    
    # Return the result
    return popup_view.result