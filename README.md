# Chat-Room
Implementation of a chat room in which people can talk in groups, Web Programming course project, Fall 2020 <br/>
- To implement this chat room, we use a server / client architecture and by using http server, we enable clients to send their messages to the server and receive other people's messages from the server. <br/>
- In general, each client, after communicating using http headers, will receive its user information from the server and will send this information in subsequent requests.
- If the user writes a message, it sends this message to the server and constantly requests the server to receive new messages, and if server receives a new message, it will send this new message to all users in response to their request.
- Note that each message must be displayed once for each user, and use long polling to reduce the number of client requests to the server in order to receive new messages.
- Each user just needs to enter its username to register and enter the chat room and this username will be sent to the server only on the first connection. Other items are not required for registration. Subsequent requests will identify the user using http headers.
- If the user disconnects from the server and reconnects, she should see the messages exchanged in between.

.
