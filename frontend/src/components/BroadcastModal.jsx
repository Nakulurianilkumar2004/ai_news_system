import { useState } from "react";
import { broadcastNews } from "../api/api"; // same place as getFavorites

export default function BroadcastModal({ news, onClose }) {
    const [channels, setChannels] = useState([]);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const toggleChannel = (ch) => {
        setChannels((prev) =>
            prev.includes(ch)
                ? prev.filter((c) => c !== ch)
                : [...prev, ch]
        );
    };

    const handleSend = async () => {
        if (channels.length === 0) {
            alert("Select at least one channel");
            return;
        }

        setLoading(true);
        setResults(null);

        try {
            // ✅ SAME PATTERN AS FAVORITES
            const res = await broadcastNews(news.id, channels);

            setResults(res.data?.results || []);

        } catch (err) {
            console.error("🔥 Broadcast Error:", err);

            const errorMsg =
                err.response?.data?.detail ||
                err.message ||
                "Broadcast failed";

            alert(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
            <div className="bg-white p-6 rounded-2xl w-96 shadow-lg">
                <h2 className="text-lg font-bold mb-4">📣 Broadcast</h2>

                {["email", "whatsapp", "linkedin", "blog", "newsletter"].map((ch) => (
                    <label key={ch} className="flex items-center gap-2 mb-2">
                        <input
                            type="checkbox"
                            checked={channels.includes(ch)}
                            disabled={loading}
                            onChange={() => toggleChannel(ch)}
                        />
                        <span className="capitalize">{ch}</span>
                    </label>
                ))}

                <button
                    onClick={handleSend}
                    disabled={loading}
                    className={`w-full py-2 rounded mt-4 text-white ${loading
                        ? "bg-gray-400"
                        : "bg-green-600 hover:bg-green-700"
                        }`}
                >
                    {loading ? "Sending..." : "Send"}
                </button>

                {results && (
                    <div className="mt-4 border-t pt-3">
                        <h3 className="font-semibold mb-2">Results:</h3>

                        {results.length === 0 ? (
                            <p className="text-sm text-gray-500">
                                No results returned
                            </p>
                        ) : (
                            results.map((r, i) => (
                                <div
                                    key={i}
                                    className="flex justify-between text-sm mb-1"
                                >
                                    <span className="capitalize">{r.channel}</span>

                                    <span
                                        className={
                                            r.status === "sent"
                                                ? "text-green-600"
                                                : "text-red-600"
                                        }
                                    >
                                        {r.status === "sent"
                                            ? "✅ Sent"
                                            : `❌ ${r.error || "Failed"}`}
                                    </span>
                                </div>
                            ))
                        )}
                    </div>
                )}

                <button
                    onClick={onClose}
                    className="w-full mt-4 text-gray-500"
                >
                    Close
                </button>
            </div>
        </div>
    );
}