def get_swagger_spec():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Cryptocurrency Market API",
            "description": "API for cryptocurrency market data using CoinGecko API. Note: Historical data is limited to the last 365 days for free API users.",
            "version": "1.0.0"
        },
        "paths": {
            "/api/symbols": {
                "get": {
                    "summary": "Get available cryptocurrency symbols",
                    "description": "Returns a list of popular cryptocurrency symbols and their current prices",
                    "responses": {
                        "200": {
                            "description": "List of symbols",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "symbol": {"type": "string"},
                                                "price": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/klines": {
                "get": {
                    "summary": "Get historical cryptocurrency data",
                    "description": "Returns historical data for a cryptocurrency with additional market information. Limited to last 365 days for free API users.",
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "query",
                            "description": "Cryptocurrency ID (e.g., bitcoin, ethereum)",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "bitcoin"
                            }
                        },
                        {
                            "name": "interval",
                            "in": "query",
                            "description": "Time interval (daily only)",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "daily"
                            }
                        },
                        {
                            "name": "start_date",
                            "in": "query",
                            "description": "Start date (YYYY-MM-DD). Will be adjusted if exceeds 365 days from end date.",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "2024-01-01"
                            }
                        },
                        {
                            "name": "end_date",
                            "in": "query",
                            "description": "End date (YYYY-MM-DD)",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "format": "date"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Historical cryptocurrency data with additional market information",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "time": {"type": "number"},
                                                        "trading_date": {"type": "string"},
                                                        "price": {"type": "number"},
                                                        "volume": {"type": "number"},
                                                        "market_cap": {"type": "number"},
                                                        "change": {"type": "number"},
                                                        "change_percent": {"type": "number"},
                                                        "name": {"type": "string"},
                                                        "symbol": {"type": "string"},
                                                        "market_cap_rank": {"type": "number"},
                                                        "total_supply": {"type": "number"},
                                                        "max_supply": {"type": "number"},
                                                        "circulating_supply": {"type": "number"},
                                                        "ath": {"type": "number"},
                                                        "atl": {"type": "number"},
                                                        "ath_change_percentage": {"type": "number"},
                                                        "atl_change_percentage": {"type": "number"}
                                                    }
                                                }
                                            },
                                            "info": {
                                                "type": "object",
                                                "properties": {
                                                    "start_date": {"type": "string"},
                                                    "end_date": {"type": "string"},
                                                    "message": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Error response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"},
                                            "info": {
                                                "type": "object",
                                                "properties": {
                                                    "start_date": {"type": "string"},
                                                    "end_date": {"type": "string"},
                                                    "error": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    } 