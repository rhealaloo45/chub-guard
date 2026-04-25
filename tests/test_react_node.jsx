// =========================
// 🔴 REACT (DEPRECATED)
// =========================

import React, { Component } from "react";
import ReactDOM from "react-dom";

// ❌ Deprecated lifecycle methods
class OldComponent extends Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
    }

    componentWillMount() { // ❌ deprecated
        console.log("Component will mount");
    }

    componentWillReceiveProps(nextProps) { // ❌ deprecated
        console.log("Receiving new props", nextProps);
    }

    componentWillUpdate() { // ❌ deprecated
        console.log("Component will update");
    }

    // ❌ string refs (deprecated)
    focusInput() {
        this.refs.myInput.focus();
    }

    render() {
        return (
            <div>
                <input type="text" ref="myInput" />
                <button onClick={() => this.setState({ count: this.state.count + 1 })}>
                    Increment
                </button>
            </div>
        );
    }
}

// ❌ ReactDOM.render (deprecated in React 18)
ReactDOM.render(<OldComponent />, document.getElementById("root"));


// =========================
// 🔴 NODE.JS (DEPRECATED)
// =========================

const fs = require("fs");
const crypto = require("crypto");
const Buffer = require("buffer").Buffer;

// ❌ new Buffer() is deprecated
const buf = new Buffer("hello world");

// ❌ fs.exists is deprecated
fs.exists("test.txt", (exists) => {
    console.log("Exists:", exists);
});

// ❌ crypto.createCipher is deprecated
const cipher = crypto.createCipher("aes192", "a password");
let encrypted = cipher.update("some clear text", "utf8", "hex");
encrypted += cipher.final("hex");

console.log("Encrypted:", encrypted);

// ❌ process.binding() is internal and deprecated
const binding = process.binding("fs");

// ❌ domain module deprecated
const domain = require("domain");
const d = domain.create();

d.run(() => {
    throw new Error("Test error inside domain");
});

// ❌ req.connection (deprecated in favor of req.socket)
const http = require("http");

http.createServer((req, res) => {
    console.log(req.connection.remoteAddress); // deprecated
    res.end("Hello");
}).listen(3000);


// =========================
// 🔴 BONUS: OLD PROMISE STYLE
// =========================

// ❌ Callback hell instead of promises/async-await
fs.readFile("file.txt", "utf8", (err, data) => {
    if (err) {
        console.error(err);
    } else {
        fs.writeFile("copy.txt", data, (err) => {
            if (err) console.error(err);
            else console.log("Done");
        });
    }
});