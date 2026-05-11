from pydantic import BaseModel, Field

class DatabaseQueryParams(BaseModel):
    table: str = Field(..., description="Table name")
    columns: list[str] = Field(default=["*"], description="Columns to select")
    where: str | None = Field(default=None, description="WHERE clause")
    limit: int = Field(default=100, ge=1, le=1000)

@tool(
    name="safe_query",
    description="Execute a safe, parameterized database query",
    parameters=DatabaseQueryParams
)
async def safe_query(args: DatabaseQueryParams):
    # args 已经通过 Pydantic 验证，类型安全
    ...
