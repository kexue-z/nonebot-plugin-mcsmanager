from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Docker(BaseModel):
    containerName: str
    image: str
    memory: int
    ports: List[str]
    extraVolumes: List
    maxSpace: None
    network: None
    io: None
    networkMode: str
    networkAliases: List
    cpusetCpus: str
    cpuUsage: int
    workingDir: str
    env: List


class TerminalOption(BaseModel):
    haveColor: bool
    pty: bool


class EventTask(BaseModel):
    autoStart: bool
    autoRestart: bool
    ignore: bool


class PingConfig(BaseModel):
    ip: str
    port: int
    type: int


class Config(BaseModel):
    nickname: str
    startCommand: str
    stopCommand: str
    cwd: str
    ie: str
    oe: str
    createDatetime: str
    lastDatetime: str
    type: str
    tag: List
    endTime: str
    fileCode: str
    processType: str
    updateCommand: str
    actionCommandList: List
    crlf: int
    docker: Docker
    enableRcon: bool
    rconPassword: str
    rconPort: int
    rconIp: str
    terminalOption: TerminalOption
    eventTask: EventTask
    pingConfig: PingConfig


class Info(BaseModel):
    currentPlayers: int
    fileLock: int
    maxPlayers: int
    openFrpStatus: bool
    playersChart: List
    version: str


class ProcessInfo(BaseModel):
    cpu: int
    memory: int
    ppid: int
    pid: int
    ctime: int
    elapsed: int
    timestamp: int


class Detail(BaseModel):
    config: Config
    info: Info
    instanceUuid: str
    processInfo: ProcessInfo
    space: int
    started: int
    status: int


class Data(BaseModel):
    maxPage: int
    pageSize: int
    data: List[Detail]


class InstanceList(BaseModel):
    """GET  /api/service/remote_service_instances"""

    status: int
    data: Data
    time: int
