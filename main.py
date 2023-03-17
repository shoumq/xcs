import pymem
import requests
import time

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(
    pm.process_handle, "client.dll").lpBaseOfDll


def offsets():
    global dwGlowObjectManager, dwLocalPlayer, dwEntityList, m_iTeamNum, m_iGlowIndex, m_iHealth

    offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
    response = requests.get(offsets).json()

    dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
    dwEntityList = int(response["signatures"]["dwEntityList"])
    dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])

    m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
    m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
    m_iHealth = int(response["netvars"]["m_iHealth"])

offsets()


def ESP():
    while True:
        player = pm.read_int(client + dwLocalPlayer)
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        if (player):
            team = pm.read_int(player + m_iTeamNum)

            for i in range(1, 32):
                entity = pm.read_int(client + dwEntityList + i * 0x10)

                if (entity):
                    try:
                        entity_team_id = pm.read_int(entity + m_iTeamNum)
                        entity_glow = pm.read_int(entity + m_iGlowIndex)
                        entity_health = pm.read_int(entity + m_iHealth)

                        if (entity_team_id != team):
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x8, float(1))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0xC, float(0))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x10, float(0))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x14, float(1))
                            
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))

                            pm.write_int(glow_manager +
                                        entity_glow * 0x38 + 0x28, 1)
                            pm.write_int(glow_manager +
                                         entity_health * 0x38 + 0x28, 1)
                        
                        else:
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x8, float(0))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0xC, float(1))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x10, float(0))
                            pm.write_float(
                                glow_manager + entity_glow * 0x38 + 0x14, float(1))
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))
                            pm.write_float(
                                glow_manager + entity_health * 0x38 + 0x14, float(1))

                            pm.write_int(glow_manager +
                                        entity_glow * 0x38 + 0x28, 1)
                            pm.write_int(glow_manager +
                                         entity_health * 0x38 + 0x28, 1)
                            
                    except:
                        print('error')

        time.sleep(0.01)
ESP()
