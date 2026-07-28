from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ការកំណត់កម្មវិធី(BaseSettings):
    បរិស្ថាន: str = Field(default="ផលិតកម្ម")
    
    ថូខិន_តេឡេក្រាម_បត: str
    តេឡេក្រាម_គេហទំព័រ_សម្ងាត់: str
    អាសយដ្ឋាន_មូលដ្ឋាន_សាធារណៈ: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


កំណត់ = ការកំណត់កម្មវិធី()
