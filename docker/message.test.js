const message = require('./message');

test('basic functionality: we should get the original message after hashing', () => {
    const input = "foo";
    const hash = message.hashMessage(input);
    expect(message.retrieveMessage(hash)).toBe(input);
})

test('return error msg', () => {
    const input = "foo";
    expect(message.retrieveMessage("aaaaaaaaaaaaa")).not.toBe(input);
})