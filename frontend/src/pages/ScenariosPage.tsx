import { useState, useEffect, useCallback } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'
import {
  RiAddLine,
  RiRefreshLine,
  RiFilterLine,
  RiListUnordered,
  RiGridFill,
  RiFlowChart
} from '@remixicon/react'
import { Button } from '@/components/common/Button'
import { ScenarioCard } from '@/components/scenarios/ScenarioCard'
import { ScenarioBuilder } from '@/components/scenarios/ScenarioBuilder'
import { WorkflowCanvas } from '@/components/workflow'
import { useWebSocketMessages } from '@/hooks/useWebSocket'
import {
  getScenarios,
  getScenario,
  createScenario,
  updateScenario,
  deleteScenario,
  duplicateScenario,
  runScenario,
  pauseScenario,
  cancelScenario,
  addScenarioStep,
  updateScenarioStep,
  deleteScenarioStep,
  reorderScenarioSteps,
  scheduleScenario,
} from '@/services/api'
import type { Scenario, ScenarioListItem, ScenarioStatus, CreateStepRequest, UpdateStepRequest } from '@/types/scenario'

type ViewMode = 'list' | 'grid' | 'workflow'
type FilterStatus = ScenarioStatus | 'all'

export function ScenariosPage() {
  const navigate = useNavigate()
  const { scenarioId } = useParams<{ scenarioId?: string }>()

  const [scenarios, setScenarios] = useState<ScenarioListItem[]>([])
  const [selectedScenario, setSelectedScenario] = useState<Scenario | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isInitialLoad, setIsInitialLoad] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all')
  const [showTemplatesOnly, setShowTemplatesOnly] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showWorkflowBuilder, setShowWorkflowBuilder] = useState(false)
  const [newScenarioName, setNewScenarioName] = useState('')
  const [newScenarioDescription, setNewScenarioDescription] = useState('')

  // Load scenarios list
  const loadScenarios = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)

      const filters: any = { limit: 50 }
      if (filterStatus !== 'all') filters.status = filterStatus
      if (showTemplatesOnly) filters.is_template = true

      const data = await getScenarios(filters)
      setScenarios(data.scenarios)
      setIsInitialLoad(false)
    } catch (error: any) {
      console.error('Error loading scenarios:', error)
      setError(error?.response?.data?.error || error?.message || 'Failed to load scenarios')
      toast.error('Failed to load scenarios')
    } finally {
      setIsLoading(false)
    }
  }, [filterStatus, showTemplatesOnly])

  // Load single scenario for builder
  const loadScenario = useCallback(async (id: string) => {
    try {
      setIsLoading(true)
      const data = await getScenario(id)
      setSelectedScenario(data)
    } catch (error: any) {
      console.error('Error loading scenario:', error)
      toast.error('Failed to load scenario')
      navigate('/scenarios')
    } finally {
      setIsLoading(false)
    }
  }, [navigate])

  // Initial load
  useEffect(() => {
    if (scenarioId) {
      loadScenario(scenarioId)
    } else {
      loadScenarios()
      setSelectedScenario(null)
    }
  }, [scenarioId, loadScenarios, loadScenario])

  // WebSocket: Scenario updates
  useWebSocketMessages('scenario_started', (message: any) => {
    loadScenarios()
    if (selectedScenario?.id === message.scenario_id) {
      loadScenario(message.scenario_id)
    }
  })

  useWebSocketMessages('scenario_progress', (message: any) => {
    // Update progress in UI if needed
    if (selectedScenario?.id === message.scenario_id) {
      loadScenario(message.scenario_id)
    }
  })

  useWebSocketMessages('scenario_completed', (message: any) => {
    toast.success('Scenario completed successfully!')
    loadScenarios()
    if (selectedScenario?.id === message.scenario_id) {
      loadScenario(message.scenario_id)
    }
  })

  useWebSocketMessages('scenario_failed', (message: any) => {
    toast.error(`Scenario failed: ${message.error || 'Unknown error'}`)
    loadScenarios()
    if (selectedScenario?.id === message.scenario_id) {
      loadScenario(message.scenario_id)
    }
  })

  // Actions
  const handleCreateScenario = async () => {
    if (!newScenarioName.trim()) {
      toast.error('Please enter a scenario name')
      return
    }

    try {
      setIsLoading(true)
      const scenario = await createScenario({
        name: newScenarioName,
        description: newScenarioDescription || undefined,
      })

      toast.success('Scenario created!')
      setShowCreateModal(false)
      setNewScenarioName('')
      setNewScenarioDescription('')
      navigate(`/scenarios/${scenario.id}`)
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to create scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRunScenario = async (id: string) => {
    try {
      setIsLoading(true)
      await runScenario(id)
      toast.success('Scenario started!')
      loadScenarios()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to start scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handlePauseScenario = async (id: string) => {
    try {
      setIsLoading(true)
      await pauseScenario(id)
      toast.success('Scenario paused')
      loadScenarios()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to pause scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancelScenario = async (id: string) => {
    try {
      setIsLoading(true)
      await cancelScenario(id)
      toast.success('Scenario cancelled')
      loadScenarios()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to cancel scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleEditScenario = (id: string) => {
    navigate(`/scenarios/${id}`)
  }

  const handleDuplicateScenario = async (id: string) => {
    try {
      setIsLoading(true)
      const scenario = await duplicateScenario(id)
      toast.success('Scenario duplicated!')
      loadScenarios()
      navigate(`/scenarios/${scenario.id}`)
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to duplicate scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteScenario = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this scenario?')) return

    try {
      setIsLoading(true)
      await deleteScenario(id)
      toast.success('Scenario deleted')
      loadScenarios()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to delete scenario')
    } finally {
      setIsLoading(false)
    }
  }

  // Builder handlers
  const handleUpdateScenario = async (data: { name?: string; description?: string }) => {
    if (!selectedScenario) return

    try {
      setIsLoading(true)
      const updated = await updateScenario(selectedScenario.id, data)
      setSelectedScenario(updated)
      toast.success('Scenario updated')
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to update scenario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddStep = async (data: CreateStepRequest) => {
    if (!selectedScenario) return

    try {
      setIsLoading(true)
      await addScenarioStep(selectedScenario.id, data)
      await loadScenario(selectedScenario.id)
      toast.success('Step added')
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to add step')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateStep = async (stepId: string, data: UpdateStepRequest) => {
    if (!selectedScenario) return

    try {
      setIsLoading(true)
      await updateScenarioStep(selectedScenario.id, stepId, data)
      await loadScenario(selectedScenario.id)
      toast.success('Step updated')
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to update step')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteStep = async (stepId: string) => {
    if (!selectedScenario) return

    try {
      setIsLoading(true)
      await deleteScenarioStep(selectedScenario.id, stepId)
      await loadScenario(selectedScenario.id)
      toast.success('Step deleted')
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to delete step')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReorderSteps = async (stepIds: string[]) => {
    if (!selectedScenario) return

    try {
      await reorderScenarioSteps(selectedScenario.id, stepIds)
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to reorder steps')
      await loadScenario(selectedScenario.id) // Reload to restore order
    }
  }

  const handleScheduleScenario = async (cron: string) => {
    if (!selectedScenario) return

    try {
      setIsLoading(true)
      await scheduleScenario(selectedScenario.id, { cron_expression: cron })
      await loadScenario(selectedScenario.id)
      toast.success('Schedule saved')
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Failed to save schedule')
    } finally {
      setIsLoading(false)
    }
  }

  // If viewing/editing a specific scenario
  if (selectedScenario) {
    return (
      <ScenarioBuilder
        scenario={selectedScenario}
        onUpdateScenario={handleUpdateScenario}
        onAddStep={handleAddStep}
        onUpdateStep={handleUpdateStep}
        onDeleteStep={handleDeleteStep}
        onReorderSteps={handleReorderSteps}
        onRun={() => handleRunScenario(selectedScenario.id)}
        onPause={() => handlePauseScenario(selectedScenario.id)}
        onResume={() => runScenario(selectedScenario.id).then(() => loadScenario(selectedScenario.id))}
        onCancel={() => handleCancelScenario(selectedScenario.id)}
        onSchedule={handleScheduleScenario}
        onBack={() => navigate('/scenarios')}
        isLoading={isLoading}
      />
    )
  }

  // Scenarios list view
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Scenarios</h1>
              <p className="mt-1 text-sm text-gray-500">
                Create and manage automation workflows
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="secondary"
                size="md"
                leftIcon={<RiFlowChart className="size-4" />}
                onClick={() => setShowWorkflowBuilder(!showWorkflowBuilder)}
              >
                {showWorkflowBuilder ? 'List View' : 'Workflow Builder'}
              </Button>
              <Button
                variant="ghost"
                size="md"
                leftIcon={<RiRefreshLine className="size-4" />}
                onClick={() => loadScenarios()}
                isLoading={isLoading}
              >
                Refresh
              </Button>
              <Button
                variant="primary"
                size="md"
                leftIcon={<RiAddLine className="size-4" />}
                onClick={() => setShowCreateModal(true)}
              >
                New Scenario
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <RiFilterLine className="size-4 text-gray-400" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value as FilterStatus)}
                  className="text-sm border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="all">All Status</option>
                  <option value="draft">Draft</option>
                  <option value="running">Running</option>
                  <option value="paused">Paused</option>
                  <option value="completed">Completed</option>
                  <option value="failed">Failed</option>
                </select>
              </div>

              <label className="flex items-center gap-2 text-sm text-gray-600">
                <input
                  type="checkbox"
                  checked={showTemplatesOnly}
                  onChange={(e) => setShowTemplatesOnly(e.target.checked)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                Templates only
              </label>
            </div>

            <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-white shadow-sm' : 'text-gray-500'}`}
              >
                <RiGridFill className="size-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-white shadow-sm' : 'text-gray-500'}`}
              >
                <RiListUnordered className="size-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Workflow Builder View */}
        {showWorkflowBuilder ? (
          <div>
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Visual Workflow Builder</h2>
              <p className="text-sm text-gray-500">Drag and drop nodes to create automation workflows</p>
            </div>
            <WorkflowCanvas
              onSave={(nodes, edges) => {
                console.log('Saving workflow:', { nodes, edges })
                toast.success('Workflow saved!')
              }}
              onRun={() => {
                toast.success('Workflow started!')
              }}
            />
          </div>
        ) : (
          <>
            {/* Error */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {/* Loading */}
            {isInitialLoad && isLoading && (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
                  <p className="mt-4 text-sm text-gray-600">Loading scenarios...</p>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!isLoading && scenarios?.length === 0 && (
              <div className="text-center py-12">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No scenarios</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Get started by creating your first automation scenario.
                </p>
                <div className="mt-6">
                  <Button variant="primary" onClick={() => setShowCreateModal(true)}>
                    <RiAddLine className="size-4 mr-2" />
                    Create Scenario
                  </Button>
                </div>
              </div>
            )}

            {/* Scenarios Grid/List */}
            {!isInitialLoad && scenarios?.length > 0 && (
              <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-4'}>
                {scenarios.map((scenario) => (
                  <ScenarioCard
                    key={scenario.id}
                    scenario={scenario}
                    onRun={handleRunScenario}
                    onPause={handlePauseScenario}
                    onCancel={handleCancelScenario}
                    onEdit={handleEditScenario}
                    onDuplicate={handleDuplicateScenario}
                    onDelete={handleDeleteScenario}
                    isLoading={isLoading}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </div>

      {/* Create Scenario Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="fixed inset-0 bg-black bg-opacity-50" onClick={() => setShowCreateModal(false)} />
          <div className="relative min-h-screen flex items-center justify-center p-4">
            <div className="relative bg-white rounded-xl shadow-xl max-w-md w-full p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Scenario</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={newScenarioName}
                    onChange={(e) => setNewScenarioName(e.target.value)}
                    placeholder="e.g., Morning outreach"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    autoFocus
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newScenarioDescription}
                    onChange={(e) => setNewScenarioDescription(e.target.value)}
                    placeholder="What does this scenario do?"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setShowCreateModal(false)}>
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  onClick={handleCreateScenario}
                  isLoading={isLoading}
                  disabled={!newScenarioName.trim()}
                >
                  Create
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
