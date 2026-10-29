"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
        }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't connect to the Math Tutor backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <main className="flex h-screen bg-[#212121] text-white">

      {/* Sidebar */}

      <aside className="hidden w-64 flex-col bg-[#171717] p-3 md:flex">

        <button
          onClick={() => setMessages([])}
          className="mb-4 rounded-lg border border-gray-700 px-4 py-3 text-left hover:bg-[#2a2a2a]"
        >
          + New chat
        </button>

        <div className="px-3 py-2 text-sm text-gray-400">
          Math Tutor
        </div>

        <div className="mt-2 rounded-lg bg-[#2a2a2a] px-3 py-2 text-sm">
          Current conversation
        </div>

        <div className="mt-auto px-3 py-3 text-xs text-gray-500">
          AI Math Tutor
          <br />
          Powered by Qwen + LoRA
        </div>

      </aside>


      {/* Main */}

      <section className="flex flex-1 flex-col">

        {/* Header */}

        <header className="border-b border-gray-700 px-6 py-4">
          <div className="mx-auto max-w-3xl">
            <h1 className="text-lg font-semibold">
              Math Tutor
            </h1>

            <p className="text-xs text-gray-400">
              Ask me any mathematics problem
            </p>
          </div>
        </header>


        {/* Messages */}

        <div className="flex-1 overflow-y-auto">

          {messages.length === 0 ? (

            <div className="flex h-full items-center justify-center px-6">

              <div className="max-w-2xl text-center">

                <div className="mb-5 text-5xl">
                  ∑
                </div>

                <h2 className="text-3xl font-semibold">
                  How can I help with math?
                </h2>

                <p className="mt-3 text-gray-400">
                  Ask a word problem, arithmetic question,
                  or anything you're stuck on.
                </p>

                <div className="mt-8 grid gap-3 sm:grid-cols-2">

                  {[
                    "Solve 25 × 17",
                    "Explain fractions",
                    "John has 5 apples and buys 3 more...",
                    "What is 144 divided by 12?"
                  ].map((example) => (

                    <button
                      key={example}
                      onClick={() => setInput(example)}
                      className="rounded-xl border border-gray-700 p-4 text-left text-sm hover:bg-[#2a2a2a]"
                    >
                      {example}
                    </button>

                  ))}

                </div>

              </div>

            </div>

          ) : (

            <div className="mx-auto max-w-3xl px-6 py-8">

              {messages.map((message, index) => (

                <div
                  key={index}
                  className={`mb-8 flex gap-4 ${message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                    }`}
                >

                  {message.role === "assistant" && (

                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-600 font-bold">
                      ∑
                    </div>

                  )}

                  <div
                    className={`max-w-[80%] rounded-2xl px-5 py-4 text-sm leading-7 ${message.role === "user"
                        ? "bg-blue-600"
                        : "bg-[#2a2a2a]"
                      }`}
                  >
                    {message.role === "assistant" ? (
                      <ReactMarkdown
                        remarkPlugins={[remarkMath]}
                        rehypePlugins={[rehypeKatex]}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      message.content
                    )}
                  </div>

                </div>

              ))}


              {loading && (

                <div className="flex gap-4">

                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 font-bold">
                    ∑
                  </div>

                  <div className="rounded-2xl bg-[#2a2a2a] px-5 py-4 text-sm text-gray-400">
                    Thinking...
                  </div>

                </div>

              )}

            </div>

          )}

        </div>


        {/* Input */}

        <div className="border-t border-gray-700 p-4">

          <div className="mx-auto max-w-3xl">

            <div className="flex items-end rounded-2xl border border-gray-600 bg-[#2a2a2a] px-4 py-3">

              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a math problem..."
                rows={1}
                className="max-h-40 flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-gray-500"
              />

              <button
                onClick={sendMessage}
                disabled={!input.trim() || loading}
                className="ml-2 rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
              >
                ↑
              </button>

            </div>

            <p className="mt-2 text-center text-xs text-gray-500">
              Math Tutor can make mistakes. Check important calculations.
            </p>

          </div>

        </div>

      </section>

    </main>
  );
}