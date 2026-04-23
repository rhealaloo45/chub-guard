// =========================
// 🔴 ANGULAR (misused inside React context, intentional chaos)
// =========================
// (This is intentionally incorrect usage to test detection systems)

import { Component } from "@angular/core"; // ❌ Angular in React app

@Component({
    selector: "app-root",
    template: "<h1>Hello</h1>"
})
export class AppComponent { }


// =========================
// 🔴 ANT DESIGN (old patterns)
// =========================

import React from "react";
import { Button, Form, Input } from "antd";

class OldForm extends React.Component {
    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => { // ❌ deprecated API
            if (!err) {
                console.log(values);
            }
        });
    };

    render() {
        const { getFieldDecorator } = this.props.form;

        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Item>
                    {getFieldDecorator("username")(<Input />)}
                </Form.Item>
                <Button htmlType="submit">Submit</Button>
            </Form>
        );
    }
}

export default Form.create()(OldForm); // ❌ deprecated HOC