
            """
            if not self.sentAudio:
                self.sentAudio = True
                print("Read")
                with open("sample.mp2", mode="rb") as file:  # b is important -> binary
                    fileContent = file.read()
                data = fileContent
                headers = {}
                headers[b"Content-Type"] = str("audio/mp2t").encode()
                headers[b"X-Session-Id"] = str(session).encode()
                headers[b"Content-Length"] = str(len(data)).encode()

                await self._send_http_request(b"--" + self.client_boundary, headers)
                chunk_size = 4096
                for i in range(0, len(data), chunk_size):
                    print(data[i : i + chunk_size])
                    self._writer.write(data[i : i + chunk_size])
                    await self._writer.drain()

                print("sending payload")
            """
