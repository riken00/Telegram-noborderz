const {Api, TelegramClient} = require('telegram');
const {StringSession} = require('telegram/sessions');

const session = new StringSession('');
const client = new TelegramClient(session, apiId, apiHash, {});

(async function run() {
    const result = await client.invoke(new Api.messages.getMessageReactionsList({
        peer: new Api.InputPeer({'piyush0012'}),
        id: 3694644,
        reaction: 'random string here',
        offset: 'random string here',
        limit: 3992090,
        }));
    console.log(result); // prints the result
})();