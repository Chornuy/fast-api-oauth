use fastApi
db.createUser(
  {
    user: "fast-api",
    pwd: "test",
    roles: [
      {
        role: "readWrite",
        db: "fast-api-websocket"
      }
    ]
  }
);
