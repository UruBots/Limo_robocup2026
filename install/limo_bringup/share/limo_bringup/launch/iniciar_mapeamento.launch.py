import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node  # <--- Importação correta

def generate_launch_description():

    # --- 1. Encontrar os caminhos para os pacotes ---
    
    # Pacote do Limo (para 'limo_start' e 'cartographer')
    limo_bringup_pkg_dir = get_package_share_directory('limo_bringup')
    
    # Pacote do Teleop (para 'teleop.launch.py')
    p9n_bringup_pkg_dir = get_package_share_directory('p9n_bringup')
    
    # --- 2. Declarar o argumento 'use_sim_time' ---
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # --- 3. Definir as Ações de Inclusão ---

    # Ação para incluir o LAUNCHER DA BASE DO LIMO
    limo_start_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(limo_bringup_pkg_dir, 'launch', 'limo_start.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Ação para incluir o LAUNCHER DO CARTOGRAPHER
    cartographer_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(limo_bringup_pkg_dir, 'launch', 'cartographer.launch.py') 
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Ação para incluir o LAUNCHER DO TELEOP
    teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(p9n_bringup_pkg_dir, 'launch', 'teleop.launch.py')
        )
        # (O código do map_saver_node foi REMOVIDO DAQUI)
    )

    # --- 4. Ação para rodar o script de salvar mapa --- (MOVIDO PARA CÁ)
    map_saver_node = Node(
        package='limo_bringup',
        executable='map_saver_listener', # <--- O nome que demos no setup.py
        name='map_saver_listener',
        output='screen'
    )
    # --- Fim do Bloco ---


    # --- 5. Retornar a Lista de Ações ---
    return LaunchDescription([
        # Declarar o argumento 'use_sim_time' neste arquivo
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        # Executar todos os nós e launchers
        limo_start_launch,
        cartographer_launch,
        teleop_launch,
        map_saver_node  # <--- Linha adicionada
    ])
