import asyncio
import time

import rakun_python


@rakun_python.Agent
class MyAgent:
    counter = 0
    start_time = time.time_ns()

    async def run(self):
        while True:
            msg = {
                # "receiver": "myagent-1",
                "data": {
                    "code": self.code,
                    "counter": self.counter,
                    "start_time": self.start_time,
                }
            }
            await self.core.message(msg)
            # await asyncio.sleep(2)

    async def receiver(self, sender, message):
        if self.counter % 10 == 0:
            diff = (time.time_ns() - self.start_time) / 1e9
            rate = self.counter / diff
            print(f"Rate {sender} {self.code}: {rate:f} msg/s")
            self.start_time = time.time_ns()
            self.counter = 0
        self.counter += 1


async def main():
    # agent = MyAgent()
    agent_manager = rakun_python.AgentManager()
    for i in range(10):
        agent_manager.register(MyAgent, f"myagent-{i}")
    await agent_manager.start()
    # await agent.core.start()


if __name__ == '__main__':
    asyncio.run(main())
