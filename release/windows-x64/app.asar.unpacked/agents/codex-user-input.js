"use strict";

const MAX_QUESTIONS = 3;
const MAX_OPTIONS = 3;
const MAX_HEADER_LENGTH = 80;
const MAX_ID_LENGTH = 80;
const MAX_QUESTION_LENGTH = 500;
const MAX_LABEL_LENGTH = 120;
const MAX_DESCRIPTION_LENGTH = 300;

function clampText(value, maxLength) {
  if (typeof value !== "string") return "";
  const normalized = value.replace(/\s+/g, " ").trim();
  return normalized.length > maxLength
    ? `${normalized.slice(0, Math.max(0, maxLength - 1))}…`
    : normalized;
}

function parseArguments(value) {
  if (value && typeof value === "object" && !Array.isArray(value)) return value;
  if (typeof value !== "string" || !value.trim()) return null;
  try {
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function normalizeOption(option) {
  if (!option || typeof option !== "object" || Array.isArray(option)) return null;
  const label = clampText(option.label, MAX_LABEL_LENGTH);
  if (!label) return null;
  return {
    label,
    description: clampText(option.description, MAX_DESCRIPTION_LENGTH),
  };
}

function normalizeQuestion(question) {
  if (!question || typeof question !== "object" || Array.isArray(question)) return null;
  const text = clampText(question.question, MAX_QUESTION_LENGTH);
  const options = Array.isArray(question.options)
    ? question.options.slice(0, MAX_OPTIONS).map(normalizeOption).filter(Boolean)
    : [];
  if (!text || options.length < 2) return null;
  return {
    header: clampText(question.header, MAX_HEADER_LENGTH),
    id: clampText(question.id, MAX_ID_LENGTH),
    question: text,
    options,
  };
}

function extractCodexUserInputRequest(payload) {
  if (!payload || typeof payload !== "object") return null;
  if (payload.type !== "function_call" || payload.name !== "request_user_input") return null;
  const args = parseArguments(payload.arguments);
  const questions = args && Array.isArray(args.questions)
    ? args.questions.slice(0, MAX_QUESTIONS).map(normalizeQuestion).filter(Boolean)
    : [];
  if (questions.length === 0) return null;
  const callId = clampText(payload.call_id || payload.id, 160);
  return normalizeCodexUserInputRequest({
    callId: callId || null,
    questions,
  });
}

function normalizeCodexUserInputRequest(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const questions = Array.isArray(value.questions)
    ? value.questions.slice(0, MAX_QUESTIONS).map(normalizeQuestion).filter(Boolean)
    : [];
  if (questions.length === 0) return null;
  const callId = clampText(value.callId, 160);
  return { callId: callId || null, questions };
}

function isMatchingCodexUserInputOutput(payload, request) {
  if (!payload || typeof payload !== "object") return false;
  if (payload.type !== "function_call_output" && payload.type !== "custom_tool_call_output") return false;
  if (!request || !request.callId) return false;
  return clampText(payload.call_id || payload.id, 160) === request.callId;
}

module.exports = {
  extractCodexUserInputRequest,
  isMatchingCodexUserInputOutput,
  normalizeCodexUserInputRequest,
};
