import Model
import UI

#git test
#git test 2
model = Model.SimpleModel()

ui = UI.MainUI(Model.rowitems,model)


data = model.Query()
ui.play()

pass

