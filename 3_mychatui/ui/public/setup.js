var bot = new ChatSDK({
  config: {
    navbar: {
      title: '智能医疗问答机器人'
    },
    robot: {
      avatar: 'http://gw.alicdn.com/tfs/TB1U7FBiAT2gK0jSZPcXXcKkpXa-108-108.jpg'
    },
    messages: [
      {
        type: 'text',
        content: {
          text: '智能医疗助理为您服务，请问有什么可以帮您？'
        }
      }
    ]
  },
  requests: {
    send: function (msg) {
      if (msg.type === 'text') {
      console.log(msg)
        return {
          url: 'http://localhost:5002/webhooks/rest/webhook',
          type: 'POST',
          data: {"sender":"sender001","message": msg.content.text}
        };
      }
    }
  },
  handlers: {
    parseResponse: function (res,requestType) {
        console.log(res)
        return myaction (res,requestType);
    }
  }
});

bot.run();