from contextlib import asynccontextmanager

from fastapi import FastAPI as ហ្វាស់អេភីអាយ
from fastapi import status as ស្ថានភាព

from អេប.អេភីអាយ.តេលេក្រាម import រ៉ោតទ័រ as តេលេក្រាម_រ៉ោតទ័រ
from អេប.ស្នូល.កំណត់រចនាសម្ព័ន្ធ import កំណត់
from អេប.សេវាកម្ម.អតិថិជន_តេឡេក្រាម import អតិថិជនតេឡេក្រាម


@asynccontextmanager
async def អាយុកាល(app: ហ្វាស់អេភីអាយ):
    វេបហ៊ុក_អាសយដ្ឋាន = f"{កំណត់.អាសយដ្ឋាន_មូលដ្ឋាន_សាធារណៈ.rstrip('/')}/telegram/webhook"
    await អតិថិជនតេឡេក្រាម.កំណត់_វេបហ៊ុក(វេបហ៊ុក_អាសយដ្ឋាន, កំណត់.តេឡេក្រាម_គេហទំព័រ_សម្ងាត់)


def បង្កើត_អេប() -> ហ្វាស់អេភីអាយ:
    អេប = ហ្វាស់អេភីអាយ(
        title="សមាគមន៍ ផៃតុន បត",
        docs_url=None if កំណត់.បរិស្ថាន == "ផលិតកម្ម" else "/docs",
        redoc_url=None if កំណត់.បរិស្ថាន == "ផលិតកម្ម" else "/redoc",
        openapi_url=None if កំណត់.បរិស្ថាន == "ផលិតកម្ម" else "/openapi.json",
        lifespan=អាយុកាល,
    )
    
    អេប.include_router(តេលេក្រាម_រ៉ោតទ័រ)

    @អេប.get("/healthz", status_code=ស្ថានភាព.HTTP_200_OK, tags=["System"])
    async def ឆែកសុខភាព():
        return {"ស្ថានភាព": "ខ្ញុំនៅរស់ទេ អរគុណដែលបានសួរសុខទុក្ខ"}

    return អេប


អេប = បង្កើត_អេប()
