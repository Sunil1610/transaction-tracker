// dbOperations.js
const Datastore = require('nedb');
const db = new Datastore({ filename: 'transactions.db', autoload: true });

const operation = process.argv[2];
const arg1 = JSON.parse(process.argv[3] || '{}');
const arg2 = JSON.parse(process.argv[4] || '{}');

if (operation === 'insert') {
    console.log(arg1);
    db.insert(arg1, (err, newDoc) => {
        if (err) throw err;
        console.log(JSON.stringify(newDoc));
    });
} else if (operation === 'update') {
    db.update(arg1, arg2, {}, (err, numReplaced) => {
        if (err) throw err;
        console.log(numReplaced);
    });
} else if (operation === 'delete') {
    db.remove(arg1, {}, (err, numRemoved) => {
        if (err) throw err;
        console.log(numRemoved);
    });
} else if (operation === 'delete_by_id') {
    db.remove({ _id: arg1 }, {}, (err, numRemoved) => {
        if (err) throw err;
        console.log(numRemoved);
    });
} else if (operation === 'find') {
    db.find(arg1, (err, docs) => {
        if (err) throw err;
        console.log(JSON.stringify(docs));
    });
}
