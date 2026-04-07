import { Plane, Hotel, Wallet, Send, Info } from 'lucide-react';
import { motion } from 'motion/react';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Plane className="text-white w-5 h-5" />
            </div>
            <h1 className="text-xl font-bold tracking-tight text-blue-900">TravelBuddy Agent</h1>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium text-slate-500">
            <span className="flex items-center gap-1"><Wallet className="w-4 h-4" /> Budget Smart</span>
            <span className="flex items-center gap-1"><Hotel className="w-4 h-4" /> Best Stays</span>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Project Info */}
        <div className="lg:col-span-1 space-y-6">
          <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Info className="w-5 h-5 text-blue-600" />
              Project Structure
            </h2>
            <div className="font-mono text-xs space-y-1 text-slate-600">
              <p>project/</p>
              <p>├── main.py</p>
              <p>├── agent/</p>
              <p>│   ├── graph.py</p>
              <p>│   ├── nodes.py</p>
              <p>│   └── state.py</p>
              <p>├── prompts/</p>
              <p>│   └── system_prompt.txt</p>
              <p>├── tools/</p>
              <p>│   └── tools.py</p>
              <p>└── config/</p>
              <p>    └── settings.py</p>
            </div>
          </section>

          <section className="bg-blue-50 p-6 rounded-2xl border border-blue-100">
            <h3 className="text-blue-900 font-semibold mb-2">How to Run</h3>
            <ol className="text-sm text-blue-800 space-y-2 list-decimal list-inside">
              <li>Install Python 3.9+</li>
              <li>Run <code className="bg-blue-100 px-1 rounded">pip install -r requirements.txt</code></li>
              <li>Set <code className="bg-blue-100 px-1 rounded">OPENAI_API_KEY</code> in <code className="bg-blue-100 px-1 rounded">.env</code></li>
              <li>Run <code className="bg-blue-100 px-1 rounded">python main.py</code></li>
            </ol>
          </section>
        </div>

        {/* Right Column: Demo UI */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[600px]">
            {/* Chat Area */}
            <div className="flex-1 p-6 space-y-4 overflow-y-auto">
              <div className="flex justify-start">
                <div className="bg-slate-100 p-4 rounded-2xl rounded-tl-none max-w-[80%] text-sm">
                  Xin chào! Tôi là TravelBuddy. Tôi có thể giúp bạn lên kế hoạch chuyến đi, tìm vé máy bay và khách sạn phù hợp với ngân sách của bạn.
                </div>
              </div>
              
              <div className="flex justify-end">
                <div className="bg-blue-600 text-white p-4 rounded-2xl rounded-tr-none max-w-[80%] text-sm">
                  Tôi muốn đi Đà Nẵng từ Hà Nội cuối tuần này, budget 5 triệu.
                </div>
              </div>

              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="flex justify-start"
              >
                <div className="bg-slate-100 p-4 rounded-2xl rounded-tl-none max-w-[80%] text-sm space-y-3">
                  <p>Đã tìm thấy thông tin cho chuyến đi của bạn:</p>
                  <div className="space-y-2">
                    <p>✈️ <strong>Chuyến bay:</strong> Vietjet Air (VJ456) - 900.000 VND (Economy, 10:30)</p>
                    <p>🏨 <strong>Khách sạn:</strong> Seaside Resort - 2.000.000 VND/đêm (4.5⭐)</p>
                    <p>💰 <strong>Tổng chi phí:</strong> 2.900.000 VND</p>
                    <p>📌 <strong>Nhận xét:</strong> Bạn vẫn còn dư 2.100.000 VND trong ngân sách. Bạn có thể nâng cấp lên khách sạn Luxury Palace hoặc dành số tiền này cho ăn uống và vui chơi!</p>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-slate-100 bg-slate-50">
              <div className="relative">
                <input 
                  type="text" 
                  placeholder="Nhập yêu cầu của bạn..." 
                  className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  disabled
                />
                <button className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-400 hover:text-blue-600 transition-colors">
                  <Send className="w-5 h-5" />
                </button>
              </div>
              <p className="text-[10px] text-center text-slate-400 mt-2 italic">
                Demo UI - Run Python project for real agent interaction
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <h4 className="text-xs font-bold text-slate-400 uppercase mb-2">Agent Logic</h4>
              <p className="text-sm">Sử dụng LangGraph để quản lý trạng thái và luồng suy luận đa bước (Multi-step reasoning).</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <h4 className="text-xs font-bold text-slate-400 uppercase mb-2">Tool Calling</h4>
              <p className="text-sm">Tự động gọi các công cụ tìm kiếm và tính toán dựa trên yêu cầu của người dùng.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
