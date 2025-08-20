import asyncio
import threading
from playwright.async_api import async_playwright

class _AsyncManager:
    def __init__(self):
        self.playwright = None
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        # A future to signal when playwright is ready
        self._playwright_ready = asyncio.Future(loop=self._loop)
        self.schedule(self._start_playwright())

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _start_playwright(self):
        self.playwright = await async_playwright().start()
        self._playwright_ready.set_result(True)

    def schedule(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def shutdown(self):
        if self.playwright:
            self.schedule(self.playwright.stop())
        self._loop.call_soon_threadsafe(self._loop.stop)

# Global instance
async_manager = _AsyncManager()
