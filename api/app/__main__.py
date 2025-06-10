import logging

import uvicorn


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[
                            logging.FileHandler("py_log.log", encoding='utf-8'),
                            logging.StreamHandler()
                        ]
                        )
    logger = logging.getLogger(__name__)

    uvicorn.run(app="app.main:app", port=8000, reload=True)
