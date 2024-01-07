



st = 'Fra:1 Mem:206.14M (Peak 494.11M) | Time:00:00.56 | Mem:192.13M, Peak:352.10M | Scene, View Layer | Updating Integrator'

x = [i for i in range(len(st)) if st.startswith('M', i)]
# x = st[3:3+5]
print(x)