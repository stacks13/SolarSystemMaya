import maya.cmds


radii = [0.383, 0.949, 1, 0.532, 11.21, 9.45, 4.01, 3.88] # radii of the planets relative to earth
moon_radius = 0.2724 # radius of earth's moon
sun_radius = 109.2 # sun's radius
time_period = [0.241, 0.615, 1, 1.88, 11.9, 29.4, 83.7, 163.7] # orbital periods of planets
names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune'] 
texture_name = "sourceimages/2k_{}.jpg" # paths to images

connections = ['coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV', 'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne']
# these are few attributes which help in getting the textures right.... got them online

"""
BAD CODE INCOMING
"""

def create_texture(n):
    """
    creates the textures for any spherical object
    """
    myShader = cmds.shadingNode('lambert', asShader=True, name=n+'_lambert') # creating lambert
    cmds.sets(name=n+"_lambertG", renderable=True, empty=True, noSurfaceShader=True) # creating lambertGroup
    cmds.connectAttr(n+'_lambert.outColor', n+"_lambertG.surfaceShader", force=True) # connecting lamberGroup to lambert
    
    cmds.surfaceShaderList(n+'_lambert', add=n+"_lambertG" )

    cmds.sets(n, e=True, forceElement=n+"_lambertG")

    myFile = cmds.shadingNode("file", name = n+'_file', asTexture=True) # creating file
    my2dTexture = cmds.shadingNode("place2dTexture", name = n+'_2dTexture', asUtility=True) # creating texture

    for i in connections:
        cmds.connectAttr(my2dTexture+'.'+i ,myFile+'.'+i, force=True)
    cmds.connectAttr(my2dTexture+'.outUV', myFile+'.uv')
    cmds.connectAttr(my2dTexture+'.outUvFilterSize', myFile+'.uvFilterSize')
    

    cmds.connectAttr(myFile+'.outColor', myShader+'.color', force=True)
    
    if n == 'sun':
        cmds.setAttr(myFile+'.fileTextureName', "sourceimages/8k_sun.jpg", type="string")
    elif n == 'background':
        cmds.setAttr(myFile+'.fileTextureName', "sourceimages/8k_background.jpg", type="string")
    else:
        # 2k images for planets
        cmds.setAttr(myFile+'.fileTextureName', texture_name.format(n), type="string")
    
    
    cmds.setAttr(my2dTexture+".rotateFrame", 90)
    
    # this is for the dark sides of the planets to be atleast dimly lit
    cmds.setAttr(myShader+".ambientColor", 0.0194805, 0.0194805, 0.0194805, type='double3')

    
def create_orbit_animation(i):
    # i'm offsetting the frames by 1500 (i may increase this) so that I can do the first part of the script
    # this creates orbits and animates them from frame 1500 to 11500
    cmds.circle(radius=i*2+5, normalY=1, normalZ=0, name=names[i]+'_orbit')
    cmds.select(names[i]+'_orbit')
    cmds.setAttr(names[i]+'_orbit.rotateY', int(i*90/8)) 
    cmds.select(names[i], names[i]+'_orbit')
    # cmds.pathAnimation(name=names[i]+'_path', fractionMode=True, follow=True, followAxis='x', upAxis='y', worldUpType='vector', worldUpVector=[0, 1, 0], inverseUp=False, bank=False, startTimeU=1500, endTimeU=1500+int(time_period[i]*10000/time_period[3]/2))
    cmds.pathAnimation(name=names[i]+'_path', fractionMode=True, follow=False, startTimeU=1500, endTimeU=1500+int(time_period[i]*10000/time_period[3]/2))
    cmds.selectKey(clear=True)
    cmds.selectKey(names[i]+'_path', keyframe=True, time=(1500, 1500+int(time_period[i]*10000/time_period[3]/2)))
    cmds.keyTangent(inTangentType='linear', outTangentType='linear')
    cmds.setInfinity(postInfinite='cycle')
    

def animate_rotation(n, period):
    """
    animates rotation of an object
    """
    cmds.select(n)
    cmds.currentTime(1)
    cmds.setKeyframe(n, breakdown=False, attribute="rotateY")
    cmds.currentTime(period)
    cmds.setAttr(n+'.rotateY', 360)
    cmds.setKeyframe(n, breakdown=False, attribute="rotateY")
    cmds.selectKey(n+'.rotateY')
    cmds.keyTangent(inTangentType='linear', outTangentType='linear')
    cmds.setInfinity(postInfinite='cycle')


def create_sun():
    """
    this creates the sun
    """
    cmds.sphere(radius=sun_radius*0.025, name='sun', axis=[0, 1.0, 0])
    cmds.setAttr('sunShape.castsShadows', 0)
    cmds.setAttr('sunShape.receiveShadows', 0)
    create_texture('sun')
    
    # this part adds the lignting of the sun
    cmds.pointLight()
    cmds.setAttr("sun_lambert.ambientColor", 1, 1, 1, type="double3")
    animate_rotation('sun', 400)
    
    
   

def create_saturn_rings():
    """
    for creating saturns rings..... more like a ring actually
    """
    cmds.torus(name='saturn_rings', axis=[0, 1.0, 0], radius=0.361, heightRatio=0.1)
    cmds.setAttr('saturn_ringsShape.castsShadows', 0)
    cmds.setAttr('saturn_ringsShape.receiveShadows', 0)
    cmds.setAttr('saturn_rings.scaleY', 0.125)

    
    myShader = cmds.shadingNode('lambert', asShader=True, name='ring_lambert') # creating lambert
    cmds.sets(name="ring_lambertG", renderable=True, empty=True, noSurfaceShader=True) # creating lambertGroup
    cmds.connectAttr('ring_lambert.outColor', "ring_lambertG.surfaceShader", force=True) # connecting lamberGroup to lambert
    
    cmds.surfaceShaderList('ring_lambert', add="ring_lambertG" )

    cmds.sets('saturn_rings', e=True, forceElement="ring_lambertG")
    
    wood = cmds.shadingNode("wood", name='ring_wood', asTexture=True) # creating file
    my3dTexture = cmds.shadingNode("place3dTexture", name='ring_3dTexture', asUtility=True) # creating texture

    cmds.connectAttr('ring_3dTexture.worldInverseMatrix', 'ring_wood.placementMatrix')

    cmds.connectAttr('ring_wood.outColor', myShader+'.color', force=True)
    cmds.parent('saturn_rings', 'saturn')

def create_moon():
    """
    create the moon
    """
    n = 'moon'
    moon_time_period = 0.0748
    cmds.sphere(name=n, axis=[0, 1.0, 0], radius=moon_radius*0.025)
    cmds.setAttr(n+'Shape.castsShadows', 0)
    cmds.setAttr(n+'Shape.receiveShadows', 0)
    cmds.select(n)
    create_texture(n)
    cmds.circle(radius=0.25, normalY=1, normalZ=0, name=n+'_orbit')
    cmds.parent('moon_orbit', 'earth')
    cmds.select(n, n+'_orbit')
    cmds.pathAnimation(name=n+'_path', fractionMode=True, follow=True, followAxis='x', upAxis='y', worldUpType='vector', worldUpVector=[0, 1, 0], inverseUp=False, bank=False, startTimeU=1, endTimeU=int(moon_time_period*10000/time_period[3]/2))
    cmds.selectKey(clear=True)
    cmds.selectKey(n+'_path', keyframe=True, time=(1, int(moon_time_period*10000/time_period[3]/2)))
    cmds.keyTangent(inTangentType='linear', outTangentType='linear')
    cmds.setInfinity(postInfinite='cycle')
    animate_rotation('moon', int(moon_time_period*10000/time_period[3]/2))

def create_planets():
    """
    loop to create the planets
    """
    for i in range(8):
        cmds.sphere(radius=radii[i]*0.025, name=names[i], axis=[0,1.0,0])
        cmds.setAttr(names[i]+'Shape.castsShadows', 0)
        cmds.setAttr(names[i]+'Shape.receiveShadows', 0)
        cmds.select(names[i])
        if i ==  5:
            create_saturn_rings()
            cmds.select(names[i])
        if i == 2:
            create_moon()
            cmds.select(names[i])
        create_texture(names[i])
        animate_rotation(names[i], 200)
        create_orbit_animation(i)

def create_background():
    n = 'background'
    cmds.sphere(radius=100, name=n, axis=[0,1.0,0])
    create_texture(n)
        
# the starting pont
create_planets()
create_sun()
create_background()
