import Model
import UI



model = Model.SimpleModel()

ui = UI.MainUI(Model.rowitems,model)


data = model.Query()
ui.play()

pass

