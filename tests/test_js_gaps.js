// Test file for GAP 2, 4 validation
import OpenAI from 'openai';

// GAP 4 test: deprecated usage 30 lines after import — should be flagged
const x = 1;
const y = 2;
const z = 3;

// This line uses a deprecated component name NOT on an import line
const result = ChatCompletion.create({ model: "gpt-3.5-turbo" });
