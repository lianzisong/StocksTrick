from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, MultiColumnListBox,\
    Button, TextBox, Widget

from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciimatics.event import KeyboardEvent

from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

import sys

class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 3 // 4,
                                       screen.width ,
                                       on_load=self._reload_list,
                                       hover_focus=True)

        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model,
            name="contacts")

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        self.fix()
        
    def _reload_list(self, new_value=None):
        self._list_view.options = self._model
        self._list_view.value = new_value

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class MulListView(Frame):
    def __init__(self, screen,columns,title,model):
        super(MulListView, self).__init__(screen,
                                       screen.height * 3 // 4,
                                       screen.width ,
                                       hover_focus=True)


        # Create the form for displaying the list of contacts.
        self._model = model
        self._last_frame = 0

        self._list_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            columns,
            options = [],
            titles= title,
            name='mainlist')

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        self.fix()


    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")
            # Force a refresh for improved responsiveness
            self._last_frame = 0

        # Now pass on to lower levels for normal handling of the event.
        return super(MulListView, self).process_event(event)

    def _update(self, frame_no):
        # Refresh the list view if needed
        last_selection = self._list_view.value
        if frame_no - self._last_frame >= self.frame_update_count or self._last_frame == 0:
            self._last_frame = frame_no
            # Update the list and try to reset the last selection.
            self._list_view.options = self._model.Query()
            self._list_view.value = last_selection  
        # Now redraw as normal
        super(MulListView, self)._update(frame_no)

    @property
    def frame_update_count(self):
        # Refresh once every 2 seconds by default.
        return 40


class MainUI:    
    def __init__(self,title,model):
        self._title = title
        self._columns = list()
        self._model = model
        for item in title:
            self._columns.append('<15%')

    
    def demo(self,screen):
        scenes = [
            Scene([MulListView(screen,self._columns,self._title,self._model)], -1),
        ]

        screen.play(scenes, stop_on_resize=True)
    
    def play(self):        
        while True:
            try:
                Screen.wrapper(self.demo, catch_interrupt=True)
                sys.exit(0)
            except ResizeScreenError:
                pass
