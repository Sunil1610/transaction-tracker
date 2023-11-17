// dbOperations.js
const Datastore = require('nedb');
const transactions_db = new Datastore({ filename: 'transactions.db', autoload: true });
const splitwise_db = new Datastore({ filename: 'splitwise_entries.db', autoload: true });

const operation = process.argv[2];
const arg1 = JSON.parse(process.argv[4] || '{}');
const arg2 = JSON.parse(process.argv[5] || '{}');
const db = process.argv[3] === 'transactions' ? transactions_db : splitwise_db;

if (operation === 'insert') {
    if ('Date' in arg1) {
        const query = {...arg1};
        delete query.Date
        arg1.Date_str = arg1.Date;
        const [day, month, year] = arg1.Date.split('/');
        arg1.Date = new Date(year, month - 1, day);
        db.findOne(query, (err, doc) => {
            if (err) throw err;
            if (doc) {
                console.log('Transaction already exists');
            } else {
                db.insert(arg1, (err, newDoc) => {
                    if (err) throw err;
                    console.log(JSON.stringify(newDoc));
                });
            }
        });
    }
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

