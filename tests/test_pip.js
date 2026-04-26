// 🛡️ Chub Guard Test File: JavaScript/TypeScript
// This file contains several deprecated patterns and architectural smells for testing.

import React from 'react';
import { Component } from '@angular/core'; // ⚠ SMELL: Mixing React and Angular

async function runTests() {
  // 1. OpenAI Legacy API
  const completion = await openai.ChatCompletion.create({
    model: "text-davinci-003", // ⚠ DEPRECATED: Model is legacy
    prompt: "Hello world",
  });

  // 2. Anthropic Legacy API
  const anthropic = new Anthropic();
  const msg = await anthropic.completions.create({
    model: "claude-2", // ⚠ DEPRECATED: Model is legacy
    prompt: `${HUMAN_PROMPT} How are you?${AI_PROMPT}`,
    max_tokens_to_sample: 300,
  });

  // 3. Browser Automation Deprecation
  const element = await page.waitForSelector('.submit-btn'); // ⚠ DEPRECATED: Use locator-based waiting

  // 4. Manual suppresses (should be ignored)
  const legacy = client.beta; // noqa: CHUB
}

console.log("Test execution complete.");
