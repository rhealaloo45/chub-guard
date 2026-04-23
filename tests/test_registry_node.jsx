// =========================
// 🔴 ANTHROPIC CLAUDE (old SDK usage style)
// =========================

const { Client } = require("@anthropic-ai/sdk"); // ❌ old import style

const client = new Client({
    apiKey: process.env.ANTHROPIC_API_KEY,
});

async function runClaude() {
    const res = await client.complete({  // ❌ deprecated method
        model: "claude-v1",
        prompt: "Hello, Claude",
        max_tokens_to_sample: 100,
    });

    console.log(res.completion);
}

runClaude();


// =========================
// 🔴 AIRTABLE (callback style instead of async/await)
// =========================

const Airtable = require("airtable");

const base = new Airtable({ apiKey: "key123" }).base("app123");

base("Users").select().eachPage(
    function page(records, fetchNextPage) {
        records.forEach(function (record) {
            console.log(record.fields);
        });
        fetchNextPage();
    },
    function done(err) {
        if (err) console.error(err);
    }
);