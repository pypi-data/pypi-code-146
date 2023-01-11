from g4camp.g4camp import g4camp

sim = g4camp(primary_generator='gps', optics=False)
sim.setDetectorHeight(1000)
sim.setDetectorRadius(500)
sim.setSkipMinMax(0.0, 0.01)
sim.setVerbose(tracking_verbose=1)
sim.configure()

# One event at 0 0 0
sim.applyGeant4Command('/gps/particle e-')
sim.applyGeant4Command('/gps/energy 1 TeV')
sim.applyGeant4Command('/gps/position 0 0 0')
sim.applyGeant4Command('/gps/direction 0 0 1')
#
for data in sim.run(n_events=1):
    particles = data.particles
    tracks = data.tracks
    print(f"\n{len(tracks):>6} tracks, {len(particles):>6} cascade starters;\n")
    
# Many events at random positions and directions
sim.applyGeant4Command('/gps/pos/type Volume')
sim.applyGeant4Command('/gps/pos/shape Cylinder')
sim.applyGeant4Command('/gps/pos/halfz 400 m')
sim.applyGeant4Command('/gps/pos/radius 400 m')
sim.applyGeant4Command('/gps/pos/center 0 0 500 m')
sim.applyGeant4Command('/gps/dir/type iso')
sim.configure()
sim.setVerbose(tracking_verbose=0)
#
for ievt, data in enumerate(sim.run(n_events=10)):
    particles = data.particles
    tracks = data.tracks
    primary = tracks[0]
    uid, gen, pdgid, x, y, z, t, E = primary
    print(f"Event #{ievt}")
    print(f"Position:   {x:.1f}, {y:.1f}, {z:.1f} m")
    print(f"{len(tracks):>6} tracks, {len(particles):>6} cascade starters;\n")
