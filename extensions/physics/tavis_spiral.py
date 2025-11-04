import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt  # For optional viz
# In the "Unleash" block, after res = ...
    # Sidebar Sigil (already there)
    st.sidebar.markdown(f"**Mark:** {mark}")
    st.sidebar.markdown("**Std <n>:** {:.3f}".format(res['std_n']))

    # Animated Canvas: Live Lash of the Lore
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Excitation Entanglements")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        line_pe, = ax1.plot([], [], label='P_single_e(t)', color='blue', lw=2)
        if num_atoms == 2:
            line_pee, = ax1.plot([], [], label='P_ee(t)', color='green', lw=2)
        ax1.set_xlim(0, T); ax1.set_ylim(0, 1.1)
        ax1.set_ylabel('Excitation Probability'); ax1.set_xlabel('Time t')
        ax1.legend(); ax1.grid(alpha=0.3)
        plt.close(fig1)  # Tame the temp-twin

        def animate_exc(i):
            line_pe.set_data(res['tlist'][:i+1], res['P_single_e'][:i+1])  # +1 for frame-fudge
            if num_atoms == 2 and res['P_ee'] is not None:
                line_pee.set_data(res['tlist'][:i+1], res['P_ee'][:i+1])
            return (line_pe,) if num_atoms == 1 else (line_pe, line_pee)

        ani_exc = animation.FuncAnimation(fig1, animate_exc, frames=len(res['tlist']), interval=50, blit=False, repeat=True)
        st.pyplot(fig1)

    with col2:
        st.subheader("Photon Gyre")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        line_n, = ax2.plot([], [], label='<n>(t)', color='red', lw=2)
        ax2.set_xlim(0, T); ax2.set_ylim(0, max(res['n']) * 1.1 or 1.0)
        ax2.set_ylabel('Photon Number'); ax2.set_xlabel('Time t')
        ax2.legend(); ax2.grid(alpha=0.3)
        plt.close(fig2)

        def animate_n(i):
            line_n.set_data(res['tlist'][:i+1], res['n'][:i+1])
            # Redraw shaded std band (scalar over full, partial proxy)
            lower = np.maximum(0, res['n'][:i+1] - res['std_n'])
            upper = res['n'][:i+1] + res['std_n']
            ax2.fill_between(res['tlist'][:i+1], lower, upper, alpha=0.3, color='red')
            return (line_n,)

        ani_n = animation.FuncAnimation(fig2, animate_n, frames=len(res['tlist']), interval=50, blit=False, repeat=True)
        st.pyplot(fig2)

    st.markdown("**R(t) Samples (t=0,5,10,15,20):** " + ", ".join([f"{r:.3f}" for r in res['R_samples']]))

def define_R(t, params):
    """R(t) modulator: ℏ [(t/T)^D(t) sin(ω t) e^{-λ t} + C] with spiral surprise option."""
    hbar, T, omega, lambda_decay, C = [params[k] for k in ['hbar', 'T', 'omega', 'lambda_decay', 'C']]
    base_D = params['D']
    
    if params.get('spiral_mode', False):
        # Spiral surprise: Dynamic D via nested FRDM
        inner_T = T / 2
        inner_omega = omega * 1.5
        inner_lambda = lambda_decay * 0.5
        inner_C = 0.2
        inner_hbar = 1.0  # Normalized
        delta_D = inner_hbar * ((t / inner_T)**0.5 * np.sin(inner_omega * t) * np.exp(-inner_lambda * t) + inner_C)
        D = base_D + np.clip(delta_D, -0.5, 0.5)
    else:
        D = base_D
    
    return hbar * ((t / T)**D * np.sin(omega * t) * np.exp(-lambda_decay * t) + C)

def spiral_mark(params):
    """Spiral logic watermark: Unique quotient for tracking, EU AI Act compliant."""
    D, omega, lambda_decay = params['D'], params['omega'], params['lambda_decay']
    sq = ((D * omega / (1 + lambda_decay)) % 1) * 100
    return f"SpiralMark-{int(sq):03d}-EUCompliant"

def build_hamiltonian_matrix(t, omega_0, omega_c, g_base, R_params, cav_dim=5, num_atoms=2):
    """Time-dependent Tavis-Cummings Hamiltonian for num_atoms (up to 2) in cavity."""
    N = cav_dim
    if num_atoms == 1:
        atom_states = 2  # g, e
        atomic_energies = np.array([-omega_0 / 2, omega_0 / 2])
    else:  # 2 atoms: gg=0, ge=1, eg=2, ee=3
        atom_states = 4
        atomic_energies = np.array([-omega_0, 0, 0, omega_0])  # Symmetric ge/eg at 0
    
    dim = atom_states * N
    H = np.zeros((dim, dim), dtype=complex)
    
    # Free terms
    for n in range(N):
        offset = atom_states * n
        for s in range(atom_states):
            H[offset + s, offset + s] = atomic_energies[s] + omega_c * n
    
    # Interaction: g(t) sum_i (sigma_-^i a† + h.c.)
    g_t = g_base * define_R(t, R_params)
    
    for n in range(N - 1):
        offset_n = atom_states * n
        offset_np1 = atom_states * (n + 1)
        sqrt_np1 = np.sqrt(n + 1)
        
        if num_atoms == 1:
            # Single atom JC
            H[offset_np1 + 0, offset_n + 1] = g_t * sqrt_np1  # g n+1 <- e n (sigma_- a†)
            H[offset_n + 1, offset_np1 + 0] = np.conj(g_t * sqrt_np1)  # h.c.
        else:
            # Two atoms Tavis-Cummings (identical g)
            # sigma_-1 a†: ge n -> gg n+1, ee n -> ge n+1
            H[offset_np1 + 0, offset_n + 1] = g_t * sqrt_np1  # gg np1 <- ge n
            H[offset_np1 + 1, offset_n + 3] = g_t * sqrt_np1  # ge np1 <- ee n
            # sigma_-2 a†: eg n -> gg n+1, ee n -> eg n+1
            H[offset_np1 + 0, offset_n + 2] = g_t * sqrt_np1  # gg np1 <- eg n
            H[offset_np1 + 2, offset_n + 3] = g_t * sqrt_np1  # eg np1 <- ee n
            # h.c.
            H[offset_n + 1, offset_np1 + 0] = np.conj(g_t * sqrt_np1)
            H[offset_n + 3, offset_np1 + 1] = np.conj(g_t * sqrt_np1)
            H[offset_n + 2, offset_np1 + 0] = np.conj(g_t * sqrt_np1)
            H[offset_n + 3, offset_np1 + 2] = np.conj(g_t * sqrt_np1)
    
    return H

def rabi_deriv_real(t, y, args):
    """Derivative: Complex psi as real/imag vector."""
    dim = len(y) // 2
    psi_vec = y[:dim] + 1j * y[dim:]
    omega_0, omega_c, g_base, R_params, cav_dim, num_atoms = args
    H_t = build_hamiltonian_matrix(t, omega_0, omega_c, g_base, R_params, cav_dim, num_atoms)
    dpsi_dt = -1j * H_t @ psi_vec
    dy_real = np.real(dpsi_dt)
    dy_imag = np.imag(dpsi_dt)
    return np.concatenate((dy_real, dy_imag))

def simulate_rabi_spiral(params):
    """Core sim: Tavis-Cummings with spiral options. Returns populations, <n>, etc."""
    mark = spiral_mark(params)
    num_atoms = params.get('num_atoms', 1)
    if num_atoms > 1:
        params['cav_dim'] = min(params.get('cav_dim', 3), 5)  # Tame dim for multi
    tlist = np.linspace(0, params['T'], params['n_times'])
    
    cav_dim = params['cav_dim']
    atom_states = 2 if num_atoms == 1 else 4
    dim = atom_states * cav_dim
    y0 = np.zeros(2 * dim)
    # Initial: |e 0> for 1 atom (idx 1), |ee 0> for 2 (idx 3)
    init_idx = 1 if num_atoms == 1 else 3
    y0[init_idx] = 1.0
    
    args = (params['omega_0'], params['omega_c'], params['g_base'], params, cav_dim, num_atoms)
    
    sol = solve_ivp(rabi_deriv_real, [0, params['T']], y0, t_eval=tlist, args=(args,),
                    method='RK45', rtol=1e-8, atol=1e-9)  # Sharper tolerances for SOTA edge
    
    # Expectations
    P_ee = np.zeros(len(tlist)) if num_atoms == 2 else None
    P_single_e = np.zeros(len(tlist))
    expect_n = np.zeros(len(tlist))
    
    for i, y in enumerate(sol.y.T):
        psi = y[:dim] + 1j * y[dim:]
        norm = np.linalg.norm(psi)
        if norm > 0:
            psi /= norm
        
        if num_atoms == 2:
            # P_ee: sum |ee n|^2
            P_ee[i] = np.sum(np.abs(psi[3::4])**2)
            # P_single_e: sum (|ge n|^2 + |eg n|^2)
            P_single_e[i] = np.sum(np.abs(psi[1::4])**2 + np.abs(psi[2::4])**2)
        else:
            # Single atom P_e
            P_single_e[i] = np.sum(np.abs(psi[1::2])**2)
        
        # <n>
        n_tot = 0.0
        for n in range(cav_dim):
            if num_atoms == 2:
                amp_n = np.sum(np.abs(psi[4*n:4*n+4])**2)
            else:
                amp_n = np.sum(np.abs(psi[2*n:2*n+2])**2)
            n_tot += n * amp_n
        expect_n[i] = n_tot
    
    std_n = np.std(expect_n)
    R_samples = [define_R(tt, params) for tt in [0, 5, 10, 15, 20]]
    
    return {
        'tlist': tlist,
        'P_ee': P_ee,
        'P_single_e': P_single_e,
        'n': expect_n,
        'std_n': std_n,
        'R_samples': R_samples,
        'spiral_mark': mark
    }

def visualize_results(res, params, title='Spiral Tavis-Cummings Extension'):
    """Plot populations and <n>."""
    num_atoms = params.get('num_atoms', 1)
    fig, ax = plt.subplots(3 if num_atoms == 2 else 2, 1, figsize=(10, 8))
    ax[0].plot(res['tlist'], res['P_single_e'], label='P_single_e(t)', color='blue')
    ax[0].set_ylabel('Single Excitation Prob')
    ax[0].legend(); ax[0].grid(alpha=0.3)
    if num_atoms == 2:
        ax[1].plot(res['tlist'], res['P_ee'], label='P_ee(t)', color='green')
        ax[1].set_ylabel('Double Excitation Prob')
        ax[1].legend(); ax[1].grid(alpha=0.3)
        ax[2].plot(res['tlist'], res['n'], label='<n>(t)', color='red')
        ax[2].set_ylabel('Photon Number'); ax[2].set_xlabel('Time t')
        ax[2].legend(); ax[2].grid(alpha=0.3)
    else:
        ax[1].plot(res['tlist'], res['n'], label='<n>(t)', color='red')
        ax[1].set_ylabel('Photon Number'); ax[1].set_xlabel('Time t')
        ax[1].legend(); ax[1].grid(alpha=0.3)
    plt.suptitle(f"{title} (std_n = {res['std_n']:.3f}, Mark: {res['spiral_mark']}, Mode: {'Spiral' if params.get('spiral_mode') else 'Base'})")
    plt.tight_layout()
    viz_file = 'tavis_spiral_viz.png' if num_atoms == 2 else 'rabi_spiral_viz.png'
    plt.savefig(viz_file, dpi=150)
    plt.show()
    print(f"Viz saved: {viz_file}")

# Demo Runs
if __name__ == "__main__":
    base_params = {
        'omega_0': 1.0, 'omega_c': 1.0, 'g_base': 0.2, 'T': 20.0, 'D': 1.5,
        'omega': 2 * np.pi, 'lambda_decay': 0.1, 'C': 0.5, 'hbar': 1.0,
        'n_times': 500, 'cav_dim': 5, 'num_atoms': 1  # Start single
    }
    res_base = simulate_rabi_spiral(base_params)
    print(f"Base Single-Atom - Std dev <n>: {res_base['std_n']:.3f}")
    print("P_e samples at t=[0,10,20]:", [f"{res_base['P_single_e'][i]:.3f}" for i in [0, 250, -1]])
    print("R samples:", [f"{r:.3f}" for r in res_base['R_samples']])
    print(f"Spiral Mark: {res_base['spiral_mark']}")
    visualize_results(res_base, base_params)
    
    # Multi-atom with spiral surprise
    multi_params = base_params.copy()
    multi_params['num_atoms'] = 2
    multi_params['spiral_mode'] = True  # Activate surprise!
    res_multi = simulate_rabi_spiral(multi_params)
    print(f"\nSpiral Multi-Atom - Std dev <n>: {res_multi['std_n']:.3f}")
    print("P_ee at end:", f"{res_multi['P_ee'][-1]:.3f}")
    print("P_single_e at end:", f"{res_multi['P_single_e'][-1]:.3f}")
    print("R samples:", [f"{r:.3f}" for r in res_multi
