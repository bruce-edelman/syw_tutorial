import paths
import numpy as np
import matplotlib.pyplot as plt
import deepdish as dd

def load_o3b_paper_run_masspdf(filename):
    """
    Generates a plot of the PPD and X% credible region for the mass distribution,
    where X=limits[1]-limits[0]
    """
    mass_1 = np.linspace(2, 100, 1000)
    mass_ratio = np.linspace(0.1, 1, 500)
    with open(filename, 'r') as _data:
        _data = dd.io.load(filename)
        marginals = _data["lines"]
    for ii in range(len(marginals['mass_1'])):
        marginals['mass_1'][ii] /= np.trapz(marginals['mass_1'][ii], mass_1)
        marginals['mass_ratio'][ii] /= np.trapz(marginals['mass_ratio'][ii], mass_ratio)
    return marginals['mass_1'], marginals['mass_ratio'], mass_1, mass_ratio


def plot_o3b_res(ax, fi, m1=False, col='tab:blue', lab='PP'):
    plpeak_mpdfs, plpeak_qpdfs, plpeak_ms, plpeak_qs = load_o3b_paper_run_masspdf(paths.data / fi)
    if m1:
        med = np.median(plpeak_mpdfs, axis=0)
        low = np.percentile(plpeak_mpdfs, 5, axis=0)
        high = np.percentile(plpeak_mpdfs, 95, axis=0)
        ax.plot(plpeak_ms, med, color=col, lw=3, alpha=0.75, label=lab)
        ax.fill_between(plpeak_ms, low, high, color=col, alpha=0.3)
        ax.plot(plpeak_ms, low, color=col, lw=0.2, alpha=0.4)
        ax.plot(plpeak_ms, high, color=col, lw=0.2, alpha=0.4)
    else:
        med = np.median(plpeak_qpdfs, axis=0)
        low = np.percentile(plpeak_qpdfs, 5, axis=0)
        high = np.percentile(plpeak_qpdfs, 95, axis=0)
        ax.plot(plpeak_qs, med, color=col, lw=3, alpha=0.75, label=lab)
        ax.fill_between(plpeak_qs, low, high, color=col, alpha=0.3)
        ax.plot(plpeak_qs, low, color=col, lw=0.2, alpha=0.4)
        ax.plot(plpeak_qs, high, color=col, lw=0.2, alpha=0.4)
    return ax

mmin = 4
mmax = 100

figx, figy = 16, 5
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(figx,figy))
axs[0] = plot_o3b_res(axs[0],'spline_20n_mass_m_iid_mag_iid_tilt_powerlaw_redshift_mass_data.h5', m1=True, lab='PLSpline', col='tab:blue')
axs[1] = plot_o3b_res(axs[1],'spline_20n_mass_m_iid_mag_iid_tilt_powerlaw_redshift_mass_data.h5', m1=False, lab='PLSpline', col='tab:blue')
axs[0].set_xlabel(r'$m_1 \,\,[M_\odot]$', fontsize=18)
axs[0].set_ylabel(r'$p_{MS}(m_1) \,\,[M_\odot^{-1}]$', fontsize=18)
axs[1].set_xlabel(r'$q$', fontsize=18)
axs[1].set_ylabel(r'$p_{MS}(q)$', fontsize=18)

for ax in axs:
    ax.grid(True, which="major", ls=":")
    ax.tick_params(labelsize=14)
    ax.set_yscale('log')
    
logticks = np.array([5,10,50,100])
axs[0].set_xticks(logticks)
axs[0].grid(True, which="major", ls=":")
axs[0].set_xscale('log')
axs[0].set_xlim(mmin, mmax)
axs[0].set_ylim(5e-5, 5e-1)
axs[1].set_xlim(mmin/mmax, 1)
axs[1].set_ylim(1e-2,1e1)

plt.suptitle(f'GWTC-3: PowerlawSpline (20 knots)', fontsize=18);
fig.tight_layout()
plt.savefig(paths.figures / 'PS_mass_distribution_plot.pdf', dpi=300);