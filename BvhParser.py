from Model.BvhNode import *
from Model.Skeleton import *
from Model.Motion import *

def readBVHfile (fileName):
    HIERARCHY = "HIERARCHY"
    OFFSET = "OFFSET"
    CHANNELS = "CHANNELS"
    JOINT_OR_END_SITE = "JOINT_OR_END"
    JOINT_OR_END_OR_RBRACE = "JOINT_OR_END_OR_RBRACE"
    LBRACE = "{"
    RBRACE = "}"
    MOTION = "MOTION"
    FRAMES = "FRAMES"
    FRAME_TIME = "FRAME TIME"

    try:
        f = open(fileName, 'r')

        read = True
        nextStr = HIERARCHY
        curNode = None
        brace = 0
        skeleton = None
        motion = None

        while True:
            if read:
                line = f.readline()

                if not line:
                    break

                line = line.strip()

                if line == "":
                    continue

            if nextStr == HIERARCHY and line.upper() == nextStr:
                nextStr = BvhNode.TYPE_ROOT
                continue
            
            elif nextStr == BvhNode.TYPE_ROOT and line.upper().split()[0].strip() == nextStr:
                nextStr = LBRACE
                skeleton = Skeleton()
                skeleton.addNode(BvhNode.TYPE_ROOT, line[len(BvhNode.TYPE_ROOT):].strip())
                curNode = skeleton.getRoot()
                continue

            elif nextStr == BvhNode.TYPE_JOINT and line.upper().split()[0].strip() == nextStr:
                nextStr = LBRACE
                name = line[len(BvhNode.TYPE_JOINT):].strip()
                curNode = skeleton.addNode(BvhNode.TYPE_JOINT, name, curNode)
                read = True
                continue

            elif nextStr == BvhNode.TYPE_END_SITE and line.upper()[:8] == nextStr:
                nextStr = LBRACE
                curNode = skeleton.addNode(BvhNode.TYPE_END_SITE, "", curNode)
                read = True
                continue

            elif nextStr == LBRACE and line == nextStr:
                nextStr = OFFSET
                brace += 1
                continue

            elif nextStr == OFFSET and line.split()[0].upper().strip() == nextStr:
                if curNode.type == BvhNode.TYPE_END_SITE:
                    nextStr = RBRACE
                else:
                    nextStr = CHANNELS

                offset = line[len(OFFSET):].strip().split()
                offset = list(map(float, offset))
                curNode.setOffset(offset)
                continue

            elif nextStr == CHANNELS and line.upper().split()[0] == nextStr:
                nextStr = JOINT_OR_END_SITE

                words = line.upper().split()
                numOfChannels = int(words[1].strip())
                channels = words[2: 2+ numOfChannels]

                curNode.setChannels(channels)
                continue

            elif nextStr == JOINT_OR_END_SITE:
                if line.split()[0].upper() == BvhNode.TYPE_JOINT:
                    nextStr = BvhNode.TYPE_JOINT

                elif line.upper()[:8] == BvhNode.TYPE_END_SITE:
                    nextStr = BvhNode.TYPE_END_SITE

                else:
                    raise Exception

                read = False
                continue
                
            elif nextStr == RBRACE and line == nextStr:
                brace -= 1

                if brace == 0:
                    nextStr = MOTION
                else:
                    nextStr = JOINT_OR_END_OR_RBRACE

                curNode = curNode.getParent()
                read = True

            elif nextStr == JOINT_OR_END_OR_RBRACE:
                read = False
                if line == RBRACE:
                    nextStr = RBRACE

                else:
                    nextStr = JOINT_OR_END_SITE
                
                continue

            elif nextStr == MOTION and line.upper() == nextStr:
                nextStr = FRAMES
                motion = Motion(skeleton)
                continue

            elif nextStr == FRAMES and line[:6].upper() == nextStr:
                motion.setFrames(int(line[6:].split()[-1]))
                nextStr = FRAME_TIME
                continue

            elif nextStr == FRAME_TIME and line[:10].upper() == "FRAME TIME" :
                motion.setFrameTime(float(line[10:].split()[-1]))
                nextStr = "DATA"
                continue

            elif nextStr == "DATA":
                data = list(map(float, line.split()))
                motion.setNextPosture(data)
                continue

            else:
                raise Exception("This is not a bvh file.(Error in \""+nextStr+"\")")

        skeleton.printHierarchy(skeleton.getRoot())

        return skeleton, motion
    except Exception as e:
        print(e) 