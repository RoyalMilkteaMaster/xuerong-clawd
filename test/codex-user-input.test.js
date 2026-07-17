"use strict";

const test = require("node:test");
const assert = require("node:assert");
const {
  extractCodexUserInputRequest,
  isMatchingCodexUserInputOutput,
} = require("../agents/codex-user-input");

test("extracts and sanitizes Codex request_user_input choices", () => {
  const request = extractCodexUserInputRequest({
    type: "function_call",
    name: "request_user_input",
    call_id: "call-1",
    arguments: JSON.stringify({
      questions: [{
        header: " Mode ",
        id: "mode",
        question: " Which mode? ",
        options: [
          { label: "Fast", description: "Quick path" },
          { label: "Safe", description: "Keep backup" },
        ],
      }],
    }),
  });

  assert.deepStrictEqual(request, {
    callId: "call-1",
    questions: [{
      header: "Mode",
      id: "mode",
      question: "Which mode?",
      options: [
        { label: "Fast", description: "Quick path" },
        { label: "Safe", description: "Keep backup" },
      ],
    }],
  });
  assert.strictEqual(
    isMatchingCodexUserInputOutput({ type: "function_call_output", call_id: "call-1" }, request),
    true
  );
});

test("rejects malformed or single-option requests", () => {
  assert.strictEqual(extractCodexUserInputRequest({ type: "function_call", name: "other" }), null);
  assert.strictEqual(extractCodexUserInputRequest({
    type: "function_call",
    name: "request_user_input",
    arguments: JSON.stringify({
      questions: [{ question: "Only one", options: [{ label: "A" }] }],
    }),
  }), null);
});
