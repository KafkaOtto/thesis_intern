import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Tuple
import seaborn as sns
import numpy as np
from matplotlib.ticker import ScalarFormatter

def format_pvalue(p: float) -> str:
    if p < 0.0001:
        return f"p < 0.0001"
    # elif p < 0.001:
    #     return f"p = {p:.1e}"
    else:
        return f"p = {p:.4f}"

def plot_effect_sizes(
        effect_sizes: List[float],
        treatment_labels: List[str],
        variable_labels: List[str],
        title: str,
        p_values: Optional[List[float]] = None,
        alpha: float = 0.05,
        figsize: Tuple[int, int] = (12, 8),
        palette: Dict[str, str] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.9,
        value_format: str = ".2f",
        show_legend: bool = True,
        significance_labels: bool = True
) -> None:
    """
    Enhanced visualization of effect sizes with professional styling.

    Args:
        effect_sizes: List of Cohen's d values
        labels: List of labels for each effect size
        title: Plot title
        p_values: Optional list of p-values for significance testing
        alpha: Significance threshold
        figsize: Figure dimensions
        palette: Custom color palette dictionary (keys: 'positive', 'negative', 'neutral')
        font_family: Font family for text elements
        grid: Whether to show grid lines
        bar_width: Width of bars
        value_format: Format string for effect size values
        show_legend: Whether to show legend
        significance_labels: Whether to show significance annotations
    """
    # Set default color palette
    if palette is None:
        palette = {
            'positive': '#4C72B0',  # Blue
            'negative': '#C44E52',  # Red
            'neutral': '#7F7F7F',  # Gray
            'sig_text': 'green',
            'ns_text': 'black'
        }
    # Set font properties
    plt.rcParams['font.family'] = font_family
    title_font = {'size': 16, 'weight': 'bold'}
    label_font = {'size': 14}

    # Create figure with constrained layout
    fig, ax = plt.subplots(figsize=figsize)

    # Determine bar colors, edge colors, and text colors
    colors = []
    text_colors = []
    annotations = []

    for d, p in zip(effect_sizes, p_values):
        if p < alpha:
            if d > 0:
                if 'accuracy' in title:
                    colors.append(palette['negative'])
                    annotations.append("↓")
                    text_colors.append(palette['sig_text'])
                else:
                    colors.append(palette['positive'])
                    annotations.append("↑")
                    text_colors.append(palette['sig_text'])
            elif d < 0:
                if 'accuracy' in title:
                    colors.append(palette['positive'])
                    annotations.append("↑")
                    text_colors.append(palette['sig_text'])
                else:
                    colors.append(palette['negative'])
                    annotations.append("↓")
                    text_colors.append(palette['sig_text'])
            else:
                colors.append(palette['neutral'])
                annotations.append("")
                text_colors.append(palette['sig_text'])
        else:
            colors.append(palette['neutral'])
            annotations.append("ns")
            text_colors.append(palette['ns_text'])

    # Create bars with improved styling
    x_pos = np.arange(len(effect_sizes))
    bars = ax.bar(
        x_pos,
        effect_sizes,
        color=colors,
        linewidth=1,
        width=bar_width,
        alpha=0.85,
        zorder=2
    )

    # Create two levels of x-axis labels
    for i, (treat, cond) in enumerate(zip(treatment_labels, variable_labels)):
        # Main treatment label (centered over group)
        if i == 0 or treatment_labels[i] != treatment_labels[i - 1]:
            group_width = treatment_labels.count(treatment_labels[i])
            group_center = i + (group_width - 1) / 2
            ax.text(group_center, -0.15, treatment_labels[i],
                    ha='center', va='top', fontsize=12, fontweight='bold',
                    transform=ax.get_xaxis_transform())

        # Condition sub-label
        ax.text(i, -0.08, variable_labels[i],
                ha='center', va='top', fontsize=10,
                transform=ax.get_xaxis_transform())
    # Add vertical lines between treatment groups
    for i in range(1, len(treatment_labels)):
        if treatment_labels[i] != treatment_labels[i-1]:
            ax.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.7)
    # Remove default x-tick labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add zero reference line
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-', zorder=1)

    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(0.5)

    # Set labels and title with improved styling
    ax.set_ylabel("Cohen's d Effect Size", **label_font)
    # ax.set_title(title, pad=20, **title_font)

    # Configure grid
    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
        ax.set_axisbelow(True)

    # Annotate bars with values and significance
    if significance_labels:
        for bar, d_val, p_val, color in zip(bars, effect_sizes, p_values, text_colors):
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            offset = 0.02 * (1 if height >= 0 else -1)
            # Calculate dynamic spacing based on plot height
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            text_spacing = y_range * 0.05  # 5% of total y-range

            # Value label position
            value_y = height + (text_spacing if height >= 0 else -text_spacing)

            # P-value label position
            p_y = height + (text_spacing * 2 if height >= 0 else -text_spacing * 2)


            # Value label
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value_y,
                f"d = {d_val:{value_format}}",
                ha='center',
                va=va,
                color=color,
                fontsize=12,
                fontweight='bold'
            )

            p_format = format_pvalue(p_val)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                p_y,
                p_format,
                ha='center',
                va=va,
                color=color,
                fontsize=12
            )


    if show_legend:
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, fc=palette['positive'],
                          label='Positive effect'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['negative'],
                          label='Negative effect'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['neutral'],
                          label='Not significant')
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper left',  # Places legend in upper right
            bbox_to_anchor=(0, 1),  # Anchors legend inside plot
            frameon=True,  # Adds a light border
            framealpha=0.8,  # Makes the legend slightly transparent
            edgecolor='gray',  # Border color
            fontsize=12,
        )

    # Adjust ylim to account for annotations
    y_min, y_max = ax.get_ylim()
    buffer = (y_max - y_min) * 0.1
    ax.set_ylim(y_min - buffer, y_max + buffer)

    # Add caption with statistical info
    # if p_values is not None:
    #     caption = f"Effect sizes with Holm-Bonferroni corrected p-values (α = {alpha})"
    #     ax.text(
    #         0.5, -0.25, caption,
    #         ha='center', va='center',
    #         transform=ax.transAxes,
    #         fontsize=9,
    #         color='#555555'
    #     )
    # Adjust margins to accommodate two-level labels
    plt.subplots_adjust(bottom=0.18)
    # plt.show()
    plt.savefig(f"plots/{title}.pdf", dpi=600)
    plt.close()


def plot_percentage_change(
        percent_changes: List[float],
        treatment_labels: List[str],
        variable_labels: List[str],
        title: str,
        p_values: Optional[List[float]] = None,
        alpha: float = 0.05,
        figsize: Tuple[int, int] = (12, 6),
        palette: Dict[str, str] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.7,
        value_format: str = ".2f",
        show_legend: bool = True,
        significance_labels: bool = True
) -> None:
    """
    Enhanced visualization of effect sizes with professional styling.

    Args:
        effect_sizes: List of Cohen's d values
        labels: List of labels for each effect size
        title: Plot title
        p_values: Optional list of p-values for significance testing
        alpha: Significance threshold
        figsize: Figure dimensions
        palette: Custom color palette dictionary (keys: 'positive', 'negative', 'neutral')
        font_family: Font family for text elements
        grid: Whether to show grid lines
        bar_width: Width of bars
        value_format: Format string for effect size values
        show_legend: Whether to show legend
        significance_labels: Whether to show significance annotations
    """
    if palette is None:
        palette = {
            'positive': '#4C72B0',  # Blue
            'negative': '#C44E52',  # Red
            'neutral': '#7F7F7F',  # Gray
            'ns_text': 'green'
        }
    # Set font properties
    plt.rcParams['font.family'] = font_family
    title_font = {'size': 16, 'weight': 'bold'}
    label_font = {'size': 14}

    # Create figure with constrained layout
    fig, ax = plt.subplots(figsize=figsize)

    # Determine bar colors, edge colors, and text colors
    colors = []
    text_colors = []
    filter_treatment_labels = []
    filter_variable_labels = []
    final_values = []

    for tl, vl, pc, pv in zip(treatment_labels, variable_labels, percent_changes, p_values):
        if pv < alpha:
            final_values.append(pc)
            filter_treatment_labels.append(tl)
            filter_variable_labels.append(vl)
            if pc < 0:
                if 'accuracy' in title:
                    colors.append(palette['negative'])
                    text_colors.append(palette['negative'])
                else:
                    colors.append(palette['positive'])
                    text_colors.append(palette['positive'])
            else:
                if 'accuracy' in title:
                    colors.append(palette['positive'])
                    text_colors.append(palette['positive'])
                else:
                    colors.append(palette['negative'])
                    text_colors.append(palette['negative'])

    # Create bars with improved styling
    x_pos = np.arange(len(final_values))
    bars = ax.bar(
        x_pos,
        final_values,
        color=colors,
        linewidth=1,
        width=bar_width,
        alpha=0.85,
        zorder=2
    )

    # Create two levels of x-axis labels
    for i, (treat, cond) in enumerate(zip(filter_treatment_labels, filter_variable_labels)):
        # Main treatment label (centered over group)
        if i == 0 or filter_treatment_labels[i] != filter_treatment_labels[i - 1]:
            group_width = filter_treatment_labels.count(filter_treatment_labels[i])
            group_center = i + (group_width - 1) / 2
            ax.text(group_center, -0.15, filter_treatment_labels[i],
                    ha='center', va='top', fontsize=12, fontweight='bold',
                    transform=ax.get_xaxis_transform())

        # Condition sub-label
        ax.text(i, -0.08, filter_variable_labels[i],
                ha='center', va='top', fontsize=12,
                transform=ax.get_xaxis_transform())
    # Add vertical lines between treatment groups
    for i in range(1, len(filter_treatment_labels)):
        if filter_treatment_labels[i] != filter_treatment_labels[i-1]:
            ax.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.7)
    # Remove default x-tick labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add zero reference line
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-', zorder=1)

    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(0.5)

    # Set labels and title with improved styling
    ax.set_ylabel("Percentage Changes(-%)", **label_font)
    # ax.set_title(title, pad=20, **title_font)

    # Configure grid
    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
        ax.set_axisbelow(True)

    # Annotate bars with values and significance
    if significance_labels:
        for bar, p_val, color in zip(bars, final_values, text_colors):
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            offset = 0.02 * (1 if height >= 0 else -1)
            # Calculate dynamic spacing based on plot height
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            text_spacing = y_range * 0.05  # 5% of total y-range

            # Value label position
            value_y = height + (text_spacing if height >= 0 else -text_spacing)

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value_y,
                f"{p_val:{value_format}}",
                ha='center',
                va=va,
                color=color,
                fontsize=12,
                fontweight='bold'
            )


    if show_legend:
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, fc=palette['positive'],
                          label='Positive effect'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['negative'],
                          label='Negative effect'),
        ]
        # Value label
        if "accuracy" in title:
            ax.legend(
                handles=legend_elements,
                loc='upper right',  # Places legend in upper right
                bbox_to_anchor=(1, 1),  # Anchors legend inside plot
                frameon=True,  # Adds a light border
                framealpha=0.8,  # Makes the legend slightly transparent
                edgecolor='gray',  # Border color
                fontsize=12,
            )
        else:
            ax.legend(
                handles=legend_elements,
                loc='upper left',  # Places legend in upper right
                bbox_to_anchor=(0, 1),  # Anchors legend inside plot
                frameon=True,  # Adds a light border
                framealpha=0.8,  # Makes the legend slightly transparent
                edgecolor='gray',  # Border color
                fontsize=12,
            )


    # Adjust ylim to account for annotations
    y_min, y_max = ax.get_ylim()
    buffer = (y_max - y_min) * 0.1
    ax.set_ylim(y_min - buffer, y_max + buffer)

    # Add caption with statistical info
    # if p_values is not None:
    #     caption = f"Effect sizes with Holm-Bonferroni corrected p-values (α = {alpha})"
    #     ax.text(
    #         0.5, -0.25, caption,
    #         ha='center', va='center',
    #         transform=ax.transAxes,
    #         fontsize=9,
    #         color='#555555'
    #     )

    ax.invert_yaxis()
    # Adjust margins to accommodate two-level labels
    plt.subplots_adjust(bottom=0.18)
    # plt.show()
    plt.savefig(f"plots/{title}.pdf", dpi=600)
    plt.close()

def group_label(row):
    if row['treatment'] == 't1' and row['variable'] == 'thresholds_base0.58':
        return 't1_control'
    else:
        return f"{row['treatment']}_{row['variable']}"

def load_box_plot(df):
    df['group'] = df.apply(group_label, axis=1)

    # Sort the groups so that 'tX_control' comes before its tX_variables
    from itertools import groupby

    grouped = sorted(df['group'].unique(), key=lambda x: (x.split('_')[0], x != f"{x.split('_')[0]}_control"))
    group_order = list(grouped)

    # Plot
    for metric in ['energy consumption', 'accuracy', 'latency']:
        plt.figure(figsize=(14, 6))
        sns.boxplot(data=df, x='group', y=metric, order=group_order)
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Boxplot of {metric} grouped by treatment (Control on left)')

        # Optional: Add vertical lines to visually separate treatment groups
        positions = [i for i, label in enumerate(group_order) if '_control' in label and i > 0]
        for pos in positions:
            plt.axvline(x=pos - 0.5, color='gray', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()



def plot_metrics_correlation_matrix(df, metrics):

    # Filter the dataframe
    filtered_df = df[metrics + ['treatment', 'variable']].dropna()

    # Create PairGrid
    g = sns.PairGrid(filtered_df, vars=metrics, hue='treatment', palette='Set1')
    g.map_upper(sns.scatterplot, alpha=0.6)
    g.map_lower(sns.kdeplot, fill=True)
    g.map_diag(sns.histplot, kde=True)
    g.add_legend(title='Treatment')

    plt.suptitle("Metrics Correlation Matrix", y=1.02)
    plt.tight_layout()
    join_metrics = "_".join(metrics)
    plt.savefig(f"{join_metrics}_metrics_correlation_matrix.png", dpi=300)
    plt.close()


def plot_gpu_percentage(
        energy_gpu_means: List[float],
        energy_total_means: List[float],
        treatment_labels: List[str],
        variable_labels: List[str],
        figsize: Tuple[int, int] = (12, 6),
        palette: Optional[Dict[str, str]] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.7,
        value_format: str = ".1f",
        show_legend: bool = True,
        significance_labels: bool = True,
        show_gpu_lines: bool = True,  # New: Control whether to show horizontal lines
        gpu_line_style: str = "--",  # New: Line style (e.g., "--", ":", "-.")
        gpu_line_color: str = "green",  # New: Line color
        gpu_line_alpha: float = 0.5,
) -> None:
    """
    Plot stacked bar chart showing GPU energy as percentage of total energy.

    Args:
        energy_gpu_means: List of mean GPU energy values
        energy_total_means: List of mean total energy values
        treatment_labels: Labels for each treatment group
        variable_labels: Labels for the variables (used in legend)
        title: Chart title
        figsize: Figure size (width, height)
        palette: Color palette dictionary with 'total' and 'gpu' keys
        font_family: Font family to use
        grid: Whether to show grid lines
        bar_width: Width of bars
        value_format: Format string for percentage values
        show_legend: Whether to show legend
        significance_labels: Whether to show percentage labels
    """
    # Set default palette if none provided
    if palette is None:
        palette = {
            'total': '#1f77b4',  # muted blue
            'gpu': '#ff7f0e'  # safety orange
        }

    # Calculate percentages
    gpu_percentages = [gpu / total * 100 for gpu, total in zip(energy_gpu_means, energy_total_means)]
    other_percentages = [100 - pct for pct in gpu_percentages]

    # Set font and style
    plt.rcParams['font.family'] = font_family
    # plt.style.use('seaborn-whitegrid' if grid else 'seaborn')

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot bars - total first (background), then GPU (foreground)
    bars_total = ax.bar(
        x=range(len(treatment_labels)),
        height=energy_total_means,
        width=bar_width,
        color=palette['total'],
        label=variable_labels[1] if len(variable_labels) > 1 else 'Total Energy'
    )

    bars_gpu = ax.bar(
        x=range(len(treatment_labels)),
        height=energy_gpu_means,
        width=bar_width,
        color=palette['gpu'],
        label=variable_labels[0] if variable_labels else 'GPU Energy'
    )

    # if show_gpu_lines:
    for idx, gpu_height in enumerate(energy_gpu_means):
        if idx == len(energy_gpu_means) - 1:
            ax.hlines(
                y=gpu_height,
                xmin=0 - bar_width / 2,  # Start at left edge of the bar
                xmax=idx + bar_width / 2,  # End at right edge of the bar
                colors="orange",
                linestyles="--",
                linewidth=2,
                zorder=300
            )

    # Create two levels of x-axis labels
    for i, (treat, cond) in enumerate(zip(treatment_labels, variable_labels)):
        # Main treatment label (centered over group)
        if i == 0 or treatment_labels[i] != treatment_labels[i - 1]:
            group_width = treatment_labels.count(treatment_labels[i])
            group_center = i + (group_width - 1) / 2
            ax.text(group_center, -0.15, treatment_labels[i],
                    ha='center', va='top', fontsize=12, fontweight='bold',
                    transform=ax.get_xaxis_transform())

        # Condition sub-label
        ax.text(i, -0.08, variable_labels[i],
                ha='center', va='top', fontsize=10,
                transform=ax.get_xaxis_transform())
    # Add vertical lines between treatment groups
    for i in range(1, len(treatment_labels)):
        if treatment_labels[i] != treatment_labels[i-1]:
            ax.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.7)
    # Remove default x-tick labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add percentage labels if enabled
    if significance_labels:
        for idx, (total, gpu, gpu_pct, other_pct) in enumerate(zip(
                energy_total_means,
                energy_gpu_means,
                gpu_percentages,
                other_percentages
        )):
            # GPU percentage (centered in GPU portion)
            ax.text(
                x=idx,
                y=gpu / 2,
                s=f"{gpu_pct:{value_format}}%",
                ha='center',
                va='center',
                color='white',
                fontweight='bold',
                fontsize=10
            )

            # Other components percentage (centered in remaining portion)
            ax.text(
                x=idx,
                y=gpu + (total - gpu) / 2,
                s=f"{other_pct:{value_format}}%",
                ha='center',
                va='center',
                color='black',
                fontsize=10
            )

    # Customize axes and labels
    ax.set_xticks([])
    ax.set_xticklabels([])
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_fontsize(10)
    ax.set_ylabel("Energy (mJ)", fontsize=12)
    # ax.set_title(title, fontsize=14, pad=20)

    # Add grid if enabled
    if grid:
        ax.grid(axis='y', linestyle=':', alpha=0.7)

    # Add legend if enabled
    if show_legend:
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, fc=palette['total'],
                          label='Other Energy'),
            plt.Rectangle((0, 0), 1, 1, fc=palette['gpu'],
                          label='GPU Energy'),
        ]
        ax.legend(
            handles=legend_elements,
            loc='lower center',  # Base location
            bbox_to_anchor=(0.5, 1.0),  # (x, y) - 0.5 is horizontal center, 1.0 is top
            frameon=True,
            framealpha=0.4,
            fontsize=10,
            ncol=2  # Arrange items in 2 columns (for compact horizontal layout)
        )

    plt.tight_layout()
    plt.savefig(f"plots/energy_gpu_percentage.pdf", dpi=300)
    plt.close()


def plot_energy_breakdown(
        energy_components: Dict[str, List[float]],
        energy_total_means: List[float],
        treatment_labels: List[str],
        variable_labels: List[str],
        component_labels: Dict[str, str],
        figsize: Tuple[int, int] = (12, 6),
        palette: Optional[Dict[str, str]] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.7,
        value_format: str = ".1f",
        show_legend: bool = True,
        show_percentage_labels: bool = True,
        min_pct_threshold: float = 1.0,
        small_pct_offset: float = 0.3,
        small_pct_marker: bool = True
) -> None:
    """
    Plot stacked bar chart showing energy breakdown by components as percentage of total energy,
    with improved handling of small percentage values.

    Args:
        energy_components: Dictionary of component names to their mean energy values
        energy_total_means: List of mean total energy values
        treatment_labels: Labels for each treatment group
        component_labels: Labels for the energy components (used in legend)
        figsize: Figure size (width, height)
        palette: Color palette dictionary with component names as keys
        font_family: Font family to use
        grid: Whether to show grid lines
        bar_width: Width of bars
        value_format: Format string for percentage values
        show_legend: Whether to show legend
        show_percentage_labels: Whether to show percentage labels
        min_pct_threshold: Minimum percentage to show label (default: 1.0)
        small_pct_offset: Offset for small percentage labels (default: 0.3)
        small_pct_marker: Whether to show markers for very small percentages (default: True)
    """
    # Set default palette if none provided
    if palette is None:
        palette = {
            'backend': '#1f77b4',  # muted blue
            'embedding': '#ff7f0e',  # safety orange
            'generation': '#2ca02c',  # cooked asparagus green
            'db': '#d62728',  # brick red
            'reranking': '#9467bd',  # muted purple,
            'system': '#17becf',
            'other': '#8c564b'  # chestnut brown
        }

    # Calculate percentages for each component
    percentages = {}
    for component, values in energy_components.items():
        percentages[component] = [val / total * 100 if total > 0 else 0
                                  for val, total in zip(values, energy_total_means)]

    # Set font and style
    plt.rcParams['font.family'] = font_family
    plt.style.use('seaborn-v0_8-whitegrid' if grid else 'seaborn')

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot stacked bars
    bottom = [0] * len(treatment_labels)
    bars = {}

    for component in energy_components.keys():
        bars[component] = ax.bar(
            x=range(len(treatment_labels)),
            height=energy_components[component],
            width=bar_width,
            bottom=bottom,
            color=palette.get(component, '#7f7f7f'),
            label=component_labels.get(component, component)
        )
        bottom = [b + h for b, h in zip(bottom, energy_components[component])]

    # Create two levels of x-axis labels
    for i, (treat, cond) in enumerate(zip(treatment_labels, variable_labels)):
        # Main treatment label (centered over group)
        if i == 0 or treatment_labels[i] != treatment_labels[i - 1]:
            group_width = treatment_labels.count(treatment_labels[i])
            group_center = i + (group_width - 1) / 2
            ax.text(group_center, -0.15, treatment_labels[i],
                    ha='center', va='top', fontsize=12, fontweight='bold',
                    transform=ax.get_xaxis_transform())

        # Condition sub-label
        ax.text(i, -0.08, variable_labels[i],
                ha='center', va='top', fontsize=10,
                transform=ax.get_xaxis_transform())

    # Add vertical lines between treatment groups
    for i in range(1, len(treatment_labels)):
        if treatment_labels[i] != treatment_labels[i - 1]:
            ax.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.7)

    # Remove default x-tick labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add percentage labels with improved handling of small values
    if show_percentage_labels:
        for i in range(len(treatment_labels)):
            cumulative_height = 0
            for component in energy_components.keys():
                component_height = energy_components[component][i]
                pct = percentages[component][i]

                # Skip if percentage is zero
                if pct == 0:
                    cumulative_height += component_height
                    continue

                # For percentages above threshold
                if pct >= min_pct_threshold:
                    # For small percentages (1-5%), place label outside with leader line
                    if pct < 5:
                        y_pos = cumulative_height + component_height

                        # Add the label outside the bar
                        ax.text(
                            x=i + small_pct_offset,
                            y=y_pos,
                            s=f"{pct:{value_format}}%",
                            ha='left',
                            va='center',
                            color='black',
                            fontsize=10,
                            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5)
                        )

                        # Add a connecting line
                        ax.plot(
                            [i + bar_width / 2, i + small_pct_offset * 0.8],
                            [y_pos, y_pos],
                            color='gray',
                            linestyle=':',
                            linewidth=0.5,
                            alpha=0.7
                        )
                    else:
                        # Normal label placement inside the bar
                        ax.text(
                            x=i,
                            y=cumulative_height + component_height / 2,
                            s=f"{pct:{value_format}}%",
                            ha='center',
                            va='center',
                            color='white' if component_height / 2 + cumulative_height < energy_total_means[
                                i] / 2 else 'black',
                            fontweight='bold',
                            fontsize=10
                        )
                # For very small but non-zero percentages
                elif small_pct_marker and pct > 0:
                    # Add a tiny dot marker
                    ax.plot(
                        i,
                        cumulative_height + component_height / 2,
                        marker='o',
                        markersize=3,
                        color='white' if component_height / 2 + cumulative_height < energy_total_means[
                            i] / 2 else 'black',
                        alpha=0.7,
                    )

                cumulative_height += component_height

    # Customize axes and labels
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set_fontsize(10)
    ax.set_ylabel("Energy (mJ)", fontsize=12)

    # Add grid if enabled
    if grid:
        ax.grid(axis='y', linestyle=':', alpha=0.7)

    # Add legend if enabled
    if show_legend:
        ax.legend(
            loc='lower center',
            bbox_to_anchor=(0.5, 1.0),
            frameon=True,
            framealpha=0.7,
            fontsize=10,
            ncol=len(energy_components)
        )

    plt.tight_layout()
    plt.savefig("plots/energy_breakdown.pdf", dpi=600, bbox_inches='tight')
    plt.close()


def plot_metrics_comparison(
        metrics_data: Dict[str, List[float]],
        treatment_labels: List[str],
        variable_labels: List[str],
        title: str,
        alpha: float = 0.05,
        figsize: Tuple[int, int] = (14, 8),
        palette: Dict[str, str] = None,
        font_family: str = "Arial",
        grid: bool = True,
        bar_width: float = 0.25,
        value_format: str = ".1f",
        show_legend: bool = True,
        significance_labels: bool = True,
        save_path: Optional[str] = None
) -> None:
    """
    Visualizes comparison between multiple metrics with professional styling.

    Args:
        metrics_data: Dictionary of metric names to percentage change values
        treatment_labels: List of treatment labels
        variable_labels: List of variable labels
        title: Plot title
        p_values: Optional dictionary of metric names to p-values
        alpha: Significance threshold
        figsize: Figure dimensions
        palette: Custom color palette dictionary
        font_family: Font family for text elements
        grid: Whether to show grid lines
        bar_width: Width of bars for each metric
        value_format: Format string for value annotations
        show_legend: Whether to show legend
        significance_labels: Whether to show significance annotations
        save_path: Optional path to save the figure
    """
    if palette is None:
        palette = {
            'energy reduction': '#4C72B0',  # Blue
            'latency reduction': '#56A3A6',  # Teal
            'accuracy changes': '#C44E52',  # Light Blue
            'ns': '#7F7F7F'  # Gray for non-significant
        }

    # Set font properties
    plt.rcParams['font.family'] = font_family
    title_font = {'size': 16, 'weight': 'bold'}
    label_font = {'size': 14}

    # Create figure with constrained layout
    fig, ax = plt.subplots(figsize=figsize)

    # Determine which metrics to plot and their order
    metric_names = list(metrics_data.keys())
    n_metrics = len(metric_names)
    n_groups = len(treatment_labels)

    # Adjust bar width based on number of metrics
    adjusted_bar_width = min(bar_width, 0.8 / n_metrics)
    group_spacing = 0.2

    # Create position arrays
    x_pos = np.arange(n_groups)
    bar_positions = [x_pos + i * adjusted_bar_width for i in range(n_metrics)]

    # Plot bars for each metric
    bars = []
    for i, metric in enumerate(metric_names):
        values = metrics_data[metric]
        color = palette.get(metric, palette['ns'])

        facecolors = [color] * len(values)

        bar = ax.bar(
            bar_positions[i],
            values,
            width=adjusted_bar_width,
            color=facecolors,
            edgecolor='white',
            linewidth=1,
            alpha=0.85,
            zorder=2,
            label=metric.capitalize()
        )
        bars.append(bar)

    # Create two levels of x-axis labels
    for i, (treat, cond) in enumerate(zip(treatment_labels, variable_labels)):
        # Main treatment label (centered over group)
        if i == 0 or treatment_labels[i] != treatment_labels[i - 1]:
            group_width = treatment_labels.count(treatment_labels[i])
            group_center = i + (group_width - 1) / 2 + (n_metrics - 1) * adjusted_bar_width / 2
            ax.text(group_center, -0.15, treatment_labels[i],
                    ha='center', va='top', fontsize=16, fontweight='bold',
                    transform=ax.get_xaxis_transform())

        # Condition sub-label
        ax.text(i + (n_metrics - 1) * adjusted_bar_width / 2, -0.08, variable_labels[i],
                ha='center', va='top', fontsize=14,
                transform=ax.get_xaxis_transform())

    # Add vertical lines between treatment groups
    for i in range(1, n_groups):
        if treatment_labels[i] != treatment_labels[i - 1]:
            line_pos = i - 0.5 + (n_metrics - 1) * adjusted_bar_width / 2
            ax.axvline(x=line_pos, color='gray', linestyle='--', alpha=0.5)

    # Remove default x-tick labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add zero reference line
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-', zorder=1)

    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(0.5)

    # Set labels and title
    ax.set_ylabel("Percentage Change (%)", **label_font)
    # ax.set_title(title, pad=20, **title_font)

    # Configure grid
    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
        ax.set_axisbelow(True)

    # Annotate bars with values
    if significance_labels:
        for metric_bars, metric_values in zip(bars, metrics_data.values()):
            for bar, value in zip(metric_bars, metric_values):
                height = bar.get_height()
                va = 'bottom' if height >= 0 else 'top'
                offset = 0.02 * (1 if height >= 0 else -1)
                y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
                text_spacing = y_range * 0.05

                value_y = height + (text_spacing if height >= 0 else -text_spacing)

                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    value_y,
                    f"{value:{value_format}}",
                    ha='center',
                    va=va,
                    color=bar.get_facecolor(),
                    fontsize=12,
                    fontweight='bold'
                )

    # Add legend
    if show_legend:
        if 't4' in save_path:
            ax.legend(
                loc='lower left',
                frameon=True,
                framealpha=0.8,
                edgecolor='gray',
                fontsize=12
            )
        elif 't2' in save_path:
            ax.legend(
                loc='upper right',
                frameon=True,
                framealpha=0.8,
                edgecolor='gray',
                fontsize=12
            )
        else:
            ax.legend(
                loc='upper left',
                frameon=True,
                framealpha=0.8,
                edgecolor='gray',
                fontsize=12
            )


    # Adjust ylim to account for annotations
    y_min, y_max = ax.get_ylim()
    buffer = (y_max - y_min) * 0.15
    ax.set_ylim(y_min - buffer, y_max + buffer)
    # ax.invert_yaxis()


    # Adjust margins to accommodate two-level labels
    plt.subplots_adjust(bottom=0.18)

    # Save or show the plot
    if save_path:
        plt.savefig(save_path, dpi=600, bbox_inches='tight')

    plt.close()
