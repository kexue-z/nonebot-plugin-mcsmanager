from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Process(BaseModel):
    cpu: int
    memory: int
    cwd: str


class Record(BaseModel):
    logined: int
    illegalAccess: int
    banips: int
    loginFailed: int


class User(BaseModel):
    uid: int
    gid: int
    username: str
    homedir: str
    shell: None


class System(BaseModel):
    user: User
    time: int
    totalmem: int
    freemem: int
    type: str
    version: str
    node: str
    hostname: str
    loadavg: List[int]
    platform: str
    release: str
    uptime: int
    cpu: float


class SystemItem(BaseModel):
    cpu: float
    mem: float


class RequestItem(BaseModel):
    value: int
    totalInstance: int
    runningInstance: int


class Chart(BaseModel):
    system: List[SystemItem]
    request: List[RequestItem]


class RemoteCount(BaseModel):
    available: int
    total: int


class Instance(BaseModel):
    running: int
    total: int


class System1(BaseModel):
    type: str
    hostname: str
    platform: str
    release: str
    uptime: float
    cwd: str
    loadavg: List[float]
    freemem: int
    cpuUsage: float
    memUsage: float
    totalmem: int
    processCpu: int
    processMem: int


class CpuMemChartItem(BaseModel):
    cpu: int
    mem: int


class RemoteItem(BaseModel):
    version: str
    process: Process
    instance: Instance
    system: System1
    cpuMemChart: List[CpuMemChartItem]
    uuid: str
    ip: str
    port: str
    prefix: str
    available: bool
    remarks: str


class Data(BaseModel):
    version: str
    specifiedDaemonVersion: str
    process: Process
    record: Record
    system: System
    chart: Chart
    remoteCount: RemoteCount
    remote: List[RemoteItem]


class Model(BaseModel):
    status: int
    data: Data
    time: int
