import Model
import UI

#git test

model = Model.SimpleModel()

ui = UI.MainUI(Model.rowitems,model)


data = model.Query()
ui.play()

pass

