import { combineReducers } from "redux";
import LayoutReducer from "./LayoutReducer";
import ScrumBoardReducer from "./ScrumBoardReducer";
import NotificationReducer from "./NotificationReducer";

const RootReducer = combineReducers({
  layout: LayoutReducer,
  scrumboard: ScrumBoardReducer,
  notification: NotificationReducer
});

export default RootReducer;
