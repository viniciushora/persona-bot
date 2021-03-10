import Mock from "../mock";
import shortId from "shortid";

let NotificationDB = {
  list:  []
};

Mock.onGet("/api/notification").reply(config => {
  const response = NotificationDB.list;
  return [200, response];
});

Mock.onPost("/api/notification/add").reply(config => {
  console.log(config);
  let notification = JSON.parse(config.data);

  NotificationDB.list.push(notification);
  const response = NotificationDB.list;
  return [200, response];
});

Mock.onPost("/api/notification/delete").reply(config => {
  let { id } = JSON.parse(config.data);
  console.log(id);

  const response = NotificationDB.list.filter(
    notification => notification.id !== id
  );
  NotificationDB.list = [...response];
  return [200, response];
});

Mock.onPost("/api/notification/delete-all").reply(config => {
  NotificationDB.list = [];
  const response = NotificationDB.list;
  return [200, response];
});
